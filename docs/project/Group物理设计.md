# Group 物理设计

> PUBLISH

Group

| 字段名              | 字段类型 | 字段属性 | 字段描述 |
| ------------------- | -------- | -------- | -------- |
| group_id            | int      | pk       |          |
| group_administrator | int      |          |          |
| group_name          | str      |          |          |
| group_info          | json     |          |          |
| status              | int      |          |          |

GroupUser

| 字段名   | 字段类型 | 字段属性 | 字段描述 |
| -------- | -------- | -------- | -------- |
| group_id | int      |          |          |
| user_id  | int      |          |          |

GroupProcedure

| 字段名       | 字段类型 | 字段属性 | 字段描述 |
| ------------ | -------- | -------- | -------- |
| group_id     | int      |          |          |
| procedure_id | int      |          |          |

GroupVenv

| 字段名   | 字段类型 | 字段属性 | 字段描述 |
| -------- | -------- | -------- | -------- |
| group_id | int      |          |          |
| app_id   | int      |          |          |

GroupDatahub

| 字段名   | 字段类型 | 字段属性 | 字段描述 |
| -------- | -------- | -------- | -------- |
| group_id | int      |          |          |
| data_id  | int      |          |          |
