# Publishing Updates

Payload for Edges:
```json
{
 "action": "<action>",
 "collection": "<edge_name>",
 "element": {
   "from": "<id_document>",
   "id": "<key>",
   "name": "<name>",
   "key": "<key>",
   "properties": {
     "key_name_1": "value_1",
     "key_name_2": "value_2"
   },
   "properties_metadata": {
     "key_name_1": {
       "description": "description_1"
     },
     "key_name_2": {
       "description": "description_2"
     }
   },
   "provider": "<driver_name>",
   "timestamp": "<timestamp>",
   "to": "<id_document>"
 },
 "type": "edges"
}
```

Payload for Collections
```json
{
 "action": "<action>",
 "collection": "<collection_name>",
 "element": {
   "id": "<key>",
   "name": "<name>",
   "key": "<key>",
   "properties": {
     "key_name_1": "value_1",
     "key_name_2": "value_2"
   },
   "properties_metadata": {
     "key_name_1": {
       "description": "description_1"
     },
     "key_name_2": {
       "description": "description_2"
     }
   },
   "provider": "<driver_name>",
   "timestamp": "<timestamp>"
 },
 "type": "collection"
}
```

Common fields:

| Field                           | Description                                                                                                                                                                                                                                                                                                                   |     
|---------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **action**                      |                                                                                                                                                                                                                                                                                                                               |
| - PATCH                         | Updates only sent properties not affecting other existing properties.                                                                                                                                                                                                                                                         |
| - CREATE                        | Create document inside collection/edge.                                                                                                                                                                                                                                                                                       |
| - UPDATE                        | Updates sent properties and remove other existing properties. If some property in payload does not exist, it will be created.                                                                                                                                                                                                 |
| - DELETE                        | Delete document inside collection/edge.                                                                                                                                                                                                                                                                                       |
| **collection**                  | Specify the name of edge/collection that you want to insert documents.                                                                                                                                                                                                                                                        |
| **element/id**                  | Its an unique hash for the same provider of collecttion. Some drivers uses an internal control identifier, others uses a MD5 hash and others uses any string. It doesn't have right or wrong models, it will vary in about how each document links with anothers and how documents know each other.                           |
| **element/name**                | String for a human identification of document.                                                                                                                                                                                                                                                                                |
| **element/provider**            | Provider is the name of who gives information. For example, the collection named "network" needs "napi" provider because it is the provider that is responsible of Insert, Update or Delete. However "comp_unit" collection needs "globomap" because it's a collection that many providers updates parts of the same document.|
| **element/timestamp**           | It's the unix timestamp that says moment that data have to be updated. If you don't have this at your data structure, generate one at runtime.                                                                                                                                                                                |
| **element/properties**          | It's an optional field. It's a dict where keys are the additional properties, with corresponding values.                                                                                                                                                                                                                      |
| **element/properties_metadata** | It's a dict, where keys are the additional properties, where the corresponding values are dictionaries where description is mandatory.                                                                                                                                                                                        |
| **element/key**                 | Mandatory at UPDATE, PATCH and DELETE actions. At CREATE it is auto set by GloboMAP API.                                                                                                                                                                                                                                      |

Specific for edges:

| Field                         | Description
|-------------------------------|-------------------------------------------------------------------|
| **element/from**              | Identifier of the source document at collection/key database.     |
| **element/to**                | Identifier of the destination document at collection/key database.|                                               

Observation: 
* A graph/layer is unique at database and also the name of collections. When documents are created the first time, **element/key** property is automatically set by GloboMAP API concatenating **element/provider** and **element/id** with underscore at middle. Therefore you can get a specific document using name of collection (**collection** property) where it is present plus **element/key** that was auto set for this particular document with a slash (/) at middle.
    * Example: For a collection named "coll" and document created into it with **element/provider**="napi" and **element/id**="2" the generated element/key property will be "napi_2". Since you can have documents in other collections with **element/key** property equals to "napi_2", you need an way to identify the "napi_2" document of "coll1" collection. GloboMAP API will understand "coll/napi_2" as this document.



