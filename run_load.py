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
#!/usr/bin/env python
import logging
import sys
from loader.loader import CoreLoader

if __name__ == '__main__':

    logging.basicConfig(
        filename='globomap-loader.log',
        level=logging.INFO,
        format='%(asctime)s %(threadName)s %(levelname)s %(message)s'
    )
    logging.getLogger("requests").setLevel(logging.WARNING)
    driver_class_name = sys.argv[1] if len(sys.argv) > 1 else None
    CoreLoader(driver_class_name).full_load()
