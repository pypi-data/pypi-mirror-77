OARepo Invenio data model
=========================

[![image][]][1]
[![image][2]][3]
[![image][4]][5]
[![image][6]][7]

Invenio base record model.

Instalation
----------
```bash
    pip install oarepo-invenio-model
```
Usage
-----
The library provides extensible Invenio base record model.

JSON Schema
-----------
Add this package to your dependencies and use it via $ref in json
schema.

### Usage example
```json
{
  "type": "object",
  "allOf": [
    {
      "properties": {
        "title": {
          "type": "string"
        }
      }
    },
    {
      "$ref": "/schemas/invenio-v1.0.0.json#/definitions/InvenioRecord"
    }
  ],
  "additionalProperties": "false"
}
```
Elastic Search Mapping
----------------------
Use `oarepo-mapping-includes` library for extanding invenio base record model mapping.
### Usage example
```json
{
  "mappings": {
    "dynamic": "strict",
    "oarepo:extends": "invenio-v1.0.0.json#/InvenioRecord",
    "properties": {
         "title": {
        "type": "text"
      }
    }
  }
}
```
 
Marshmallow
-----------
You can extense your schema with Invenio base model schema by inheriting from `InvenioRecordMetadataSchemaV1Mixin`.
### Usage example
```python
class SampleSchemaV1(InvenioRecordMetadataSchemaV1Mixin):
    title = fields.String(validate=validate.Length(min=5), required=True)
```
  [image]: https://img.shields.io/github/license/oarepo/invenio-oarepo-invenio-model.svg
  [1]: https://github.com/oarepo/invenio-oarepo-invenio-model/blob/master/LICENSE
  [2]: https://img.shields.io/travis/oarepo/invenio-oarepo-invenio-model.svg
  [3]: https://travis-ci.org/oarepo/invenio-oarepo-invenio-model
  [4]: https://img.shields.io/coveralls/oarepo/invenio-oarepo-invenio-model.svg
  [5]: https://coveralls.io/r/oarepo/invenio-oarepo-invenio-model
  [6]: https://img.shields.io/pypi/v/invenio-oarepo-dc.svg
  [7]: https://pypi.org/pypi/invenio-oarepo-dc