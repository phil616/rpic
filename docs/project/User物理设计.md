# User Structure

> PUBLISH

User

| 字段名    | 字段类型 | 字段属性 | 字段描述   |
| --------- | -------- | -------- | ---------- |
| user_id   | int      |          | id         |
| username  | str      |          | name       |
| password  | str      |          | auth       |
| user_info | json     |          | json email |
| status    | bool     |          | bool /1/0  |

UserRole

| 字段名     | 字段类型 | 字段属性 | 字段描述 |
| ---------- | -------- | -------- | -------- |
| user_id    | int      |          |          |
| user_roles | str      |          |          |

UserScope

| 字段名      | 字段类型 | 字段属性 | 字段描述 |
| ----------- | -------- | -------- | -------- |
| user_role   | str      |          |          |
| user_scopes | str      |          |          |



