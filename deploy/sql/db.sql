SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

drop schema if exists simple_feedback;
create schema simple_feedback collate utf8mb4_unicode_ci;

-- 创建用户
DROP USER IF EXISTS 'fb_user'@'%';
CREATE USER 'fb_user'@'%' IDENTIFIED BY 'fb_pwd@2025';
GRANT ALL PRIVILEGES ON simple_feedback.* TO 'fb_user'@'%';
FLUSH PRIVILEGES;

-- 切换到数据库
USE simple_feedback;

drop table if exists fb_dict_data;
create table fb_dict_data
(
    dict_code   bigint auto_increment comment '字典编码' primary key,
    dict_sort   int(4)       default 0   null comment '字典排序',
    dict_label  varchar(100) default ''  null comment '字典标签/I18n键',
    dict_value  varchar(100) default ''  null comment '字典键值',
    dict_type   varchar(100) default ''  null comment '字典类型',
    is_default  char         default 'N' null comment '是否默认（Y是 N否）',
    status      char         default '0' null comment '状态（0正常 1停用）',
    create_by   varchar(64)  default ''  null comment '创建者',
    create_time datetime                 null comment '创建时间',
    update_by   varchar(64)  default ''  null comment '更新者',
    update_time datetime                 null comment '更新时间',
    remark      varchar(500)             null comment '备注'
) comment '字典数据表';

insert into fb_dict_data
values (1, 1, 'feedback_type_question', 'question', 'feedback_type', 'Y', '0', 'admin', sysdate(), '', null, '咨询类');
insert into fb_dict_data
values (2, 2, 'feedback_type_issue', 'issue', 'feedback_type', 'Y', '0', 'admin', sysdate(), '', null, 'bug类');
/* value 同 owner 的 code */
insert into fb_dict_data
values (3, 1, 'owner_type', 'wehailer', 'owner_type', 'Y', '0', 'admin', sysdate(), '', null, 'app类');
insert into fb_dict_data
values (4, 2, 'owner_type', 'wesim', 'owner_type', 'Y', '0', 'admin', sysdate(), '', null, 'app类');

drop table if exists fb_dict_type;
create table fb_dict_type
(
    dict_id     bigint auto_increment comment '字典主键'
        primary key,
    dict_name   varchar(100) default ''  null comment '字典名称',
    dict_type   varchar(100) default ''  null comment '字典类型',
    status      char         default '0' null comment '状态（0正常 1停用）',
    create_by   varchar(64)  default ''  null comment '创建者',
    create_time datetime                 null comment '创建时间',
    update_by   varchar(64)  default ''  null comment '更新者',
    update_time datetime                 null comment '更新时间',
    remark      varchar(500)             null comment '备注',
    constraint dict_type unique (dict_type)
) comment '字典类型表';

insert into fb_dict_type
values (1, '反馈类型', 'feedback_type', '0', 'admin', sysdate(), '', null, '问题反馈类型');
/* 设置归属类型, 用于限制使用范围, owner的叶子节点 */
insert into fb_dict_type
values (2, '归属类型', 'owner_type', '0', 'admin', sysdate(), '', null, '设备归属类型');

drop table if exists fb_owner;
create table fb_owner
(
    owner_id    bigint auto_increment comment '归属者ID'
        primary key,
    owner_name  varchar(50)              not null comment '归属者名称',
    parent_id   bigint       default 0   null comment '父归属者ID',
    order_num   int(4)       default 0   null comment '显示顺序',
    code        varchar(200) default ''  null comment '归属者代码',
    visible     char         default '0' null comment '归属者可视状态（0显示 1隐藏）',
    status      char         default '0' null comment '归属者状态（0正常 1停用）',
    icon        varchar(100) default '#' null comment '归属者图标',
    create_by   varchar(64)  default ''  null comment '创建者',
    create_time datetime                 null comment '创建时间',
    update_by   varchar(64)  default ''  null comment '更新者',
    update_time datetime                 null comment '更新时间',
    remark      varchar(500) default ''  null comment '备注'
) comment '设备归属表';

insert into fb_owner
values (1, 'APP', 0, 1, 'app', '0', '0', '', 'admin', sysdate(), '', null, 'APP');
insert into fb_owner
values (100, 'WeHailer', 1, 1, 'wehailer', '0', '0', '', 'admin', sysdate(), '', null, 'WeHailer');
insert into fb_owner
values (101, 'WeSIM', 1, 2, 'wesim', '0', '0', '', 'admin', sysdate(), '', null, 'WeSIM');

drop table if exists fb_device;
create table fb_device
(
    device_id   bigint auto_increment comment '设备ID'
        primary key,
    device_key  varchar(200) default ''  null comment '设备key',
    status      char         default '0' null comment '设备状态（0正常 1停用）',
    create_by   varchar(64)  default ''  null comment '创建者',
    create_time datetime                 null comment '创建时间',
    update_by   varchar(64)  default ''  null comment '更新者',
    update_time datetime                 null comment '更新时间',
    remark      varchar(500) default ''  null comment '备注',
    unique uk_device (device_key)
) comment "设备表";

drop table if exists fb_device_owner;
create table fb_device_owner
(
    device_id bigint(20) not null comment "设备ID",
    owner_id  bigint(20) not null comment "归属者ID",
    primary key (device_id, owner_id)
) comment "设备归属映射表";


drop table if exists fb_message;
create table fb_message
(
    msg_id      bigint auto_increment comment '消息ID'
        primary key,
    top_id      bigint       default 0  null comment '顶层消息ID',
    parent_id   bigint       default 0  null comment '父消息ID',
    owner_id    bigint                  not null comment '归属ID',
    device_id   bigint                  not null comment '设备ID',
    content     text         default '' comment '内容',
    meta        text         default '{}' comment '元数据, json字符串',
    status      char         default '0' null comment '状态（0正常 1已解决）',
    del_flag    char         default '0' null comment '删除标志（0代表存在 2代表删除）',
    create_by   varchar(64)  default '' null comment '创建者',
    create_time datetime                null comment '创建时间',
    update_by   varchar(64)  default '' null comment '更新者',
    update_time datetime                null comment '更新时间',
    remark      varchar(500) default '' null comment '备注',
    index idx_top_parent (top_id, parent_id),
    index idx_owner_device (owner_id, device_id),
    index idx_update_time (update_time)
) comment "信息反馈表";

drop table if exists fb_user;
create table fb_user
(
    user_id     bigint(20)  not null auto_increment comment '用户ID',
    user_name   varchar(30) not null comment '用户账号',
    nick_name   varchar(30) not null comment '用户昵称',
    user_type   varchar(2)   default '00' comment '用户类型（00系统用户）',
    email       varchar(50)  default '' comment '用户邮箱',
    phone_number varchar(11)  default '' comment '手机号码',
    sex         char(1)      default '0' comment '用户性别（0男 1女 2未知）',
    avatar      varchar(100) default '' comment '头像地址',
    password    varchar(100) default '' comment '密码',
    status      char(1)      default '0' comment '帐号状态（0正常 1停用）',
    del_flag    char(1)      default '0' comment '删除标志（0代表存在 2代表删除）',
    login_ip    varchar(128) default '' comment '最后登录IP',
    login_date  datetime comment '最后登录时间',
    create_by   varchar(64)  default '' comment '创建者',
    create_time datetime comment '创建时间',
    update_by   varchar(64)  default '' comment '更新者',
    update_time datetime comment '更新时间',
    remark      varchar(500) default null comment '备注',
    primary key (user_id)
) engine = innodb comment = '用户信息表';
#   auto_increment = 100 comment = '用户信息表';
-- admin@2025
insert into fb_user values(1, 'admin', 'admin', '00', '', '', '2', '', '$2b$10$Dul694SFQROmjySbVqDRne9uYx4a/24A.w.vKHp5ihHR5V3lO.vHe', '0', '0', '127.0.0.1', sysdate(), 'admin', sysdate(), '', null, '管理员');
