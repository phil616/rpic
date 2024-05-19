/*
 Navicat Premium Data Transfer

 Source Server         : localMySQL
 Source Server Type    : MySQL
 Source Server Version : 50736 (5.7.36)
 Source Host           : localhost:3306
 Source Schema         : rpics

 Target Server Type    : MySQL
 Target Server Version : 50736 (5.7.36)
 File Encoding         : 65001

 Date: 18/05/2024 21:22:38
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for endpoint_procedure
-- ----------------------------
DROP TABLE IF EXISTS `endpoint_procedure`;
CREATE TABLE `endpoint_procedure`  (
  `create_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
  `update_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '更新人',
  `create_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '创建人',
  `endpoint_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Endpoint ID, primary key',
  `namespace` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Namespace',
  `mount_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Mount Path',
  `procedure_id` int(11) NOT NULL COMMENT 'Procedure ID',
  PRIMARY KEY (`endpoint_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'Endpoint Procedure' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for group
-- ----------------------------
DROP TABLE IF EXISTS `group`;
CREATE TABLE `group`  (
  `create_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
  `update_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '更新人',
  `create_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '创建人',
  `group_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Group ID, primary key',
  `group_administrator` int(11) NOT NULL COMMENT 'Group Administrator',
  `group_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Group Name',
  `group_info` json NOT NULL COMMENT 'Group Info',
  `group_status` int(11) NOT NULL COMMENT 'Group Status',
  PRIMARY KEY (`group_id`) USING BTREE,
  UNIQUE INDEX `uid_group_group_i_c564a5`(`group_id`, `group_name`) USING BTREE,
  INDEX `group_id_index`(`group_id`) USING BTREE,
  INDEX `group_name_index`(`group_name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'Group Table' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for group_datahub
-- ----------------------------
DROP TABLE IF EXISTS `group_datahub`;
CREATE TABLE `group_datahub`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
  `update_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '更新人',
  `create_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '创建人',
  `group_id` int(11) NOT NULL COMMENT 'Group ID',
  `datahub_id` int(11) NOT NULL COMMENT 'datahub_id,assigned by cp',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'Group Datahub' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for group_procedure
-- ----------------------------
DROP TABLE IF EXISTS `group_procedure`;
CREATE TABLE `group_procedure`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
  `update_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '更新人',
  `create_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '创建人',
  `group_id` int(11) NOT NULL COMMENT 'Group ID',
  `procedure_id` int(11) NOT NULL COMMENT 'Group Procedure',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'Group Procedure' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for group_subapp
-- ----------------------------
DROP TABLE IF EXISTS `group_subapp`;
CREATE TABLE `group_subapp`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
  `update_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '更新人',
  `create_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '创建人',
  `group_id` int(11) NOT NULL COMMENT 'Group ID',
  `subapp_id` int(11) NOT NULL COMMENT 'subapp_id,assigned by cp',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'Group Subapp' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for group_user
-- ----------------------------
DROP TABLE IF EXISTS `group_user`;
CREATE TABLE `group_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
  `update_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '更新人',
  `create_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '创建人',
  `group_id` int(11) NOT NULL COMMENT 'Group ID',
  `user_id` int(11) NOT NULL COMMENT 'Group User',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'Group User' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for procedure
-- ----------------------------
DROP TABLE IF EXISTS `procedure`;
CREATE TABLE `procedure`  (
  `create_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
  `update_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '更新人',
  `create_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '创建人',
  `procedure_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Procedure ID, primary key',
  `procedure_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Script or Package',
  `procedure_creator` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Procedure Creator',
  `procedure_group_id` int(11) NOT NULL COMMENT 'Procedure Group ID',
  `memory_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Memory ID',
  `disk_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Disk ID',
  `execute_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'MOUNT AND EXECUTE' COMMENT 'Execute Type:[MOUNT ONLY,EXECUTE ONLY,MOUNT AND EXECUTE]',
  `endpoint_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'Endpoint ID',
  `procedure_raw` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'raw body',
  PRIMARY KEY (`procedure_id`) USING BTREE,
  UNIQUE INDEX `uid_procedure_procedu_b8954f`(`procedure_id`, `procedure_type`) USING BTREE,
  INDEX `procedure_id_index`(`procedure_id`) USING BTREE,
  INDEX `procedure_type_index`(`procedure_type`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'Procedure Table' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for procedure_execute
-- ----------------------------
DROP TABLE IF EXISTS `procedure_execute`;
CREATE TABLE `procedure_execute`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
  `update_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '更新人',
  `create_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '创建人',
  `procedure_id` int(11) NOT NULL COMMENT 'Procedure ID',
  `executed_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Executed By',
  `executed_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT 'Executed At',
  `executed_from` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Executed From',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'Procedure Execute' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for procedure_info
-- ----------------------------
DROP TABLE IF EXISTS `procedure_info`;
CREATE TABLE `procedure_info`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
  `update_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '更新人',
  `create_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '创建人',
  `procedure_id` int(11) NOT NULL COMMENT 'Procedure ID',
  `procedure_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Procedure Name',
  `procedure_decrypt_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Procedure Decrypt Key',
  `procedure_encrypt_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'AES' COMMENT 'Procedure Encrypt Type AES/SM4',
  `procedure_size` int(11) NULL DEFAULT NULL COMMENT 'Procedure Size',
  `procedure_extra` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'Procedure Info',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'Procedure Info' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for role_scope
-- ----------------------------
DROP TABLE IF EXISTS `role_scope`;
CREATE TABLE `role_scope`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
  `update_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '更新人',
  `create_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '创建人',
  `user_role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'User Roles',
  `role_scopes` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Role Scopes',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'Role Scope' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for subapp
-- ----------------------------
DROP TABLE IF EXISTS `subapp`;
CREATE TABLE `subapp`  (
  `create_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
  `update_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '更新人',
  `create_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '创建人',
  `subapp_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'subapp id',
  `subapp_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'subapp host',
  `subapp_port` int(11) NOT NULL DEFAULT 8000 COMMENT 'subapp port',
  `subapp_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT 'status 0:not onlone 1:online',
  `subapp_latest_report` datetime(6) NOT NULL COMMENT 'last report time',
  PRIMARY KEY (`subapp_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'subapp info' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `create_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
  `update_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '更新人',
  `create_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '[system]' COMMENT '创建人',
  `user_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'User ID, primary key',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Username',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Password',
  `user_info` json NOT NULL COMMENT 'User Info',
  `user_status` int(11) NOT NULL COMMENT 'User Status',
  `user_roles` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'User Roles',
  PRIMARY KEY (`user_id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE,
  UNIQUE INDEX `uid_user_user_id_abe5fe`(`user_id`, `username`) USING BTREE,
  INDEX `user_id_index`(`user_id`) USING BTREE,
  INDEX `username_index`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'User Table' ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
