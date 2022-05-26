import subprocess as sp
import time
from os.path import expanduser as expand_user
from resource.base import BaseResource

from docstring import docstring
from lib.http import HTTPMethod
from lib.parser import json_parser, property_parser, xml_parser, yaml_parser
from lib.response import (BadRequestResponse, BaseResponse, ContentResponse,
                          NoContentResponse, NotFoundResponse)
from schema.config import (ConfigActionResponseSchema,
                           ConfigParameterResponseSchema, ConfigRequestSchema,
                           ConfigResourceResponseSchema)
from utils.datetime import datetime_to_str
from utils.exception import extract_info
from utils.json import loads
from utils.sequence import is_list, wrap

MSG_NOT_FOUND = "{} {} not found"
MSG_NOT_ACCESSIBLE = "{} {} not accessible"
MSG_NO_CONTENT = "No content to apply configurations with the {{request}}"
MSG_NOT_VALID = "Not valid JSON for {}"


class ConfigResource(BaseResource):
    tag = {"name": "config", "description": "Configuration at run-time."}
    routes = ("/config",)
    parsers = {
        "json": json_parser,
        "properties": property_parser,
        "xml": xml_parser,
        "yaml": yaml_parser,
    }

    schema = {
        "actions": ConfigActionResponseSchema,
        "parameters": ConfigParameterResponseSchema,
        "resources": ConfigResourceResponseSchema,
    }

    @docstring(source="config/post.yaml")
    def on_post(self, req, resp):
        req_data = req.media or {}
        cfg_req_sh = ConfigRequestSchema(
            many=is_list(req_data), method=HTTPMethod.POST
        )
        resp_data, valid = cfg_req_sh.validate(data=req_data)
        if valid:
            req_data_wrap = wrap(req_data)
            if len(req_data_wrap) > 0:
                for config in req_data_wrap:
                    for cfg, cfg_list in config.items():
                        for data in wrap(cfg_list):
                            output = self.__operations(cfg, data)
                            if isinstance(output, BaseResponse):
                                output.add(resp)
                            else:
                                output_data = data.copy()
                                _id = output_data.pop("id", None)
                                output.update(
                                    id=_id,
                                    data=output_data,
                                    timestamp=datetime_to_str(),
                                )
                                schema = self.schema[cfg]
                                schema_obj = schema(
                                    many=False,
                                    method=HTTPMethod.POST,
                                    unknown="INCLUDE",
                                )
                                resp_data, valid = schema_obj.validate(
                                    data=output
                                )
                                if valid:
                                    ContentResponse(output).add(resp)
                                else:
                                    resp_data.add(resp)
            else:
                NoContentResponse(MSG_NO_CONTENT, request=req_data).apply(resp)
        else:
            resp_data.apply(resp)

    def __operations(self, cfg, data):
        output = {}
        if cfg == "actions":
            output = self.__actions(data)
        elif cfg == "parameters":
            output = self.__parameters(data)
        elif cfg == "resources":
            output = self.__resources(data)
        return output

    def __actions(self, data):
        cmd = data.get("cmd", None)
        daemon = data.get("daemon", False)
        output_format = data.get("output_format", "plain")
        output = {"type": "action"}
        run = " ".join([cmd] + wrap(data.get("args", [])))
        start = time.time()
        proc = self.__run_cmd(cmd=run, daemon=daemon, output=output)
        if daemon:
            output.update(error=False, return_code=0)
        else:
            output.update(
                error=proc.returncode != 0,
                return_code=proc.returncode,
                duration=time.time() - start,
            )
            self.__set_std(proc.stdout, output, "stdout", output_format)
            self.__set_std(proc.stderr, output, "stderr", output_format)
        return output

    def __parameters(self, data):
        schema = data.get("schema", None)
        source = data.get("source", None)
        path = []
        for p in wrap(data.get("path", [])):
            try:
                np = int(p)
            except ValueError:
                np = p
            path.append(np)
        value = data.get("value", None)
        output = {"type": "parameter"}
        try:
            source = expand_user(source)
            output.update(
                self.parsers.get(schema)(schema, source, path, value)
            )
            return output
        except FileNotFoundError as exception:
            _msg = MSG_NOT_FOUND.format("Source", source)
            self.log.exception(_msg, exception)
            return NotFoundResponse(
                _msg, exception, type="parameter", data=data
            )
        except Exception as exception:
            _msg = (MSG_NOT_ACCESSIBLE.format("Source", source),)
            self.log.exception(_msg, exception)
            return BadRequestResponse(
                exception, message=_msg, type="parameter", data=data
            )

    def __resources(self, data):
        path = data.get("path", None)
        content = data.get("content", None)
        output = {"type": "resource"}
        try:
            fix_path = expand_user(path)
            with open(fix_path, "w") as file:
                file.write(content)
            output.update(path=path, content=content)
            return output
        except FileNotFoundError as exception:
            _msg = MSG_NOT_FOUND.format("Path", path)
            self.log.exception(_msg, exception)
            return NotFoundResponse(
                _msg, exception, type="resource", data=data
            )
        except Exception as exception:
            _msg = MSG_NOT_ACCESSIBLE.format("Path", path)
            self.log.exception(_msg, exception)
            return BadRequestResponse(
                exception, message=_msg, type="resource", data=data
            )

    def __set_std(self, data, output, key, output_format):
        if data:
            data = data.strip()
            if output_format == "plain":
                output[key] = data
            elif output_format == "lines":
                output[key] = data.splitlines()
            else:
                try:
                    output[key] = loads(data)
                except Exception as exception:
                    _msg = MSG_NOT_VALID.format(key)
                    self.log.exception(_msg, exception)
                    output.update(
                        description=_msg, exception=extract_info(exception)
                    )
                    output[key] = data

    def __run_cmd(self, cmd, daemon, output):
        if not daemon:
            return sp.run(
                cmd,
                check=False,
                shell=True,
                stdout=sp.PIPE,
                stderr=sp.PIPE,
                universal_newlines=True,
            )
        else:
            return sp.Popen(
                cmd,
                shell=True,
                stdout=sp.PIPE,
                stderr=sp.PIPE,
                start_new_session=True,
            )
