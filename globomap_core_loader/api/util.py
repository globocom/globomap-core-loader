"""
   Copyright 2017 Globo.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import json

from jsonspec.validators import load


def json_validate(json_file):

    with open(json_file) as data_file:
        data = json.load(data_file)
        validator = load(data)

    return validator


def validate(error):
    msg = list()
    if error.flatten():
        for pointer, reasons in error.flatten().items():
            msg.append({
                'error_pointer': pointer,
                'error_reasons': list(reasons)
            })
    else:
        msg.append({
            'error_pointer': error[0],
            'error_reasons': list(error[1])
        })
    res = {
        'errors': msg
    }

    return res
