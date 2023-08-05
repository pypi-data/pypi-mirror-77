# Application

Application's properties
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created** | **datetime** | Creation time | [optional] [readonly] 
**id** | **str** | application service id | [optional] [readonly] 
**name** | **str** | application name | 
**description** | **str** | Application description text | [optional] 
**category** | **str** | application category | 
**image** | **str** | image registry path and name | [optional] 
**image_username** | **str** | registry username | [optional] 
**image_password** | **str** | registry password | [optional] 
**image_credentials_type** | **str** | type of credentials for image | [optional] 
**environments** | [**list[Environment]**](Environment.md) | List of environments | [optional] 
**org_id** | **str** | organisation id | 
**contact_email** | **str** | Administrator contact email | [optional] 
**port** | **int** | The transport layer port the application listens on for requests. E.g. if the application listens for HTTP requests on the standard port, port 80, set this to 80.  | [optional] [default to 5000]
**healthcheck_uri** | **str** | health check URI | [optional] 
**roles** | [**RoleList**](RoleList.md) |  | [optional] 
**definitions** | [**list[Definition]**](Definition.md) | List of definitions | [optional] 
**assignments** | [**list[ApplicationAssignment]**](ApplicationAssignment.md) | Controls the Organisations which have access to Environments of this Application.  | [optional] 
**owned** | **bool** | Whether this Application is owned by the provided organisation.  | [optional] 
**maintained** | **bool** | Whether this Application has an Environment maintained by the provided organisation.  | [optional] 
**assigned** | **bool** | Whether an Environment is assigned to this Application.  | [optional] 
**updated** | **datetime** | Update time | [optional] [readonly] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


