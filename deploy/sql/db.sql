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
)
    comment '字典数据表';

insert into fb_dict_data values (1, 1, 'feedback_type_question', 'question', 'feedback_type', 'Y', '0', 'admin', sysdate(), '', null, '咨询类');
insert into fb_dict_data values (2, 2, 'feedback_type_issue', 'issue', 'feedback_type', 'Y', '0', 'admin', sysdate(), '', null, 'bug类');
/* value 同 owner 的 code */
insert into fb_dict_data values (3, 1, 'owner_type', 'wehailer', 'owner_type', 'Y', '0', 'admin', sysdate(), '', null, 'app类');
insert into fb_dict_data values (4, 2, 'owner_type', 'wesim', 'owner_type', 'Y', '0', 'admin', sysdate(), '', null, 'app类');

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
)
    comment '字典类型表';

insert into fb_dict_type values (1, '反馈类型', 'feedback_type', '0', 'admin', sysdate(), '', null, '问题反馈类型');
/* 设置归属类型, 用于限制使用范围, owner的叶子节点 */
insert into fb_dict_type values (2, '归属类型', 'owner_type', '0', 'admin', sysdate(), '', null, '设备归属类型');

drop table if exists fb_owner;
create table fb_owner
(
    owner_id     bigint auto_increment comment '归属者ID'
        primary key,
    owner_name   varchar(50)              not null comment '归属者名称',
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
)
    comment '设备归属表';

insert into fb_owner values (1, 'APP', 0, 1, 'app', '0', '0', '', 'admin', sysdate(), '', null, 'APP');
insert into fb_owner values (100, 'WeHailer', 1, 1, 'wehailer', '0', '0', '', 'admin', sysdate(), '', null, 'WeHailer');
insert into fb_owner values (101, 'WeSIM', 1, 2, 'wesim', '0', '0', '', 'admin', sysdate(), '', null, 'WeSIM');

drop table if exists fb_device;
create table fb_device
(
    device_id    bigint auto_increment comment '设备ID'
        primary key,
    device_key   varchar(200) default ''  null comment '设备key',
    status      char         default '0' null comment '设备状态（0正常 1停用）',
    create_by   varchar(64)  default ''  null comment '创建者',
    create_time datetime                 null comment '创建时间',
    update_by   varchar(64)  default ''  null comment '更新者',
    update_time datetime                 null comment '更新时间',
    remark      varchar(500) default ''  null comment '备注',
    unique uk_device(device_key)
)
    comment "设备表";

drop table if exists fb_device_owner;
create table fb_device_owner
(
    device_id bigint(20) not null comment "设备ID",
    owner_id bigint(20) not null comment "归属者ID",
    primary key(device_id, owner_id)
)
    comment "设备归属映射表";


drop table if exists fb_message;
create table fb_message
(
    msg_id      bigint auto_increment comment '消息ID'
        primary key,
    top_id      bigint       default 0   null comment '顶层消息ID',
    parent_id   bigint       default 0   null comment '父消息ID',
    owner_id   bigint not null     comment '归属ID',
    device_id   bigint not null     comment '设备ID',
    content     text default ''     comment '内容',
    meta        text default '{}'   comment '元数据, json字符串',
    create_by   varchar(64)  default ''  null comment '创建者',
    create_time datetime                 null comment '创建时间',
    update_by   varchar(64)  default ''  null comment '更新者',
    update_time datetime                 null comment '更新时间',
    remark      varchar(500) default ''  null comment '备注',
    index idx_top_parent(top_id, parent_id),
    index idx_owner_device(owner_id, device_id)
)
    comment "信息反馈表";

