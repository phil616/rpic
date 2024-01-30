# Procedure 物理设计

> PUBLISH

Procedure

| 字段名             | 字段类型 | 字段属性 | 字段描述                    |
| ------------------ | -------- | -------- | --------------------------- |
| procedure_id       | int      |          | id                          |
|                    |          |          |                             |
| procedure_type     | str      |          | script/package              |
| procedure_creator  | int      |          | userid                      |
| memory_id          | json     |          | memory id                   |
| disk_id            | int      |          | disk id                     |
| execute_type       | str      |          | onlymount/mount-exe/onlyexe |
| procedure_group_id | str      |          | group_id                    |
| endpoint_id        |          |          | endpoint id                 |
| status             |          |          | running/mounting/dead       |

ProcedureInfo

| 字段名                 | 字段类型 | 字段属性 | 字段描述     |
| ---------------------- | -------- | -------- | ------------ |
| procedure_id           | int      |          | id           |
| procedure_name         | str      |          | name         |
| procedure_decrypt_key  | str      |          | key          |
| procedure_encrypt_type | str      |          | aes/other    |
| procedure_size         | int      |          | size/memsize |
| procedure_extra        | json     |          | json         |

ProcedureExecute

| 字段名        | 字段类型 | 字段属性 | 字段描述           |
| ------------- | -------- | -------- | ------------------ |
| procedure_id  | int      |          | ID                 |
| executed_by   | int      |          | 用户               |
| executed_at   | datetime |          | 时间               |
| executed_from |          |          | 从哪个虚拟机运行的 |

EndpointProcedure

| 字段名         | 字段类型 | 字段属性 | 字段描述           |
| -------------- | -------- | -------- | ------------------ |
| endpoint_id    |          |          | id                 |
| param_number   |          |          | 参数的数量         |
| openapi_schema |          |          | schama             |
| namespace      |          |          | group prefix       |
| mount_path     |          |          | fastapi mount path |

