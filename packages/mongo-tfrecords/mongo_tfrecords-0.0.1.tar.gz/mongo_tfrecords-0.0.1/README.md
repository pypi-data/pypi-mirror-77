<!--
 Copyright 2020 Vadim Sharay <vadimsharay@gmail.com>

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 -->

# mongo-tfrecords

mongo-tfrecords - Library that exports mongodb data to tensorflow files (tf-record)

## Installation

`pip install mongo-tfrecords`


## Usage examples

```
# from bash
python3 -m mongo_tfrecords 

# api docs
python3 -m mongo_tfrecords --help
```

```
# from python
from mongo_tfrecords import export

export(
    collection="test", 
    database="mongodb://user:password@hostname:27017/database_name?authSource=admin",
    path="/path/to/",
    files_template="{}.tfrecord",
    count_per_file=100000,  # count items per one file
    features=["field1", "field2"],  # fields [int, float, string, bytes, ...],
    skip=10,
    limit=10000,
    verbose=True,  # show progress bar
)
```

## License

Apache License 2.0 (See [LICENSE](https://github.com/felixfire/mongo-tfrecords/blob/master/LICENSE/))

Copyright 2020, Vadim Sharay
