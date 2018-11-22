[当前页面](/bkapi/) 必须登录才能访问，另外有一个 [权限测试页面](/bkapi/permission_test/) 必须拥有 `permission_test` 权限才能访问，若要访问请到 [统一权限管理](http://bk.tencent.com/campus/permission_center/apply/) 页面申请 `权限测试页面` 权限

* 内部 OAuth API（仅能在服务器内部网络访问）

    * [get_app_access_token](/bkapi/get_app_access_token/)：获取代表应用权限的 `access_token`
    * [get_user_access_token](/bkapi/get_user_access_token/)：通过用户的 `openid` 和 `openkey` 获取用户的 `access_token`（包括 `refresh_token`）
    * [refresh_user_access_token](/bkapi/refresh_user_access_token/)：通过 `refresh_token` 重新获取获取用户的 `access_token`

* 用户权限 API

    * [get_permissions](/bkapi/get_permissions/)：通过用户的 `openid` 获取用户在当前应用拥有的权限

* 获取用户信息 API

    * [get_user_info](/bkapi/get_user_info/)：通过用户的 `openid` 和 `openkey` 获取用户 QQ 号和头像
    * [get_openid_openkey](/bkapi/get_openid_openkey/)：通过 Cookie 中的 `uin` 和 `skey` 获取用户的 `openid` 和 `openkey`
    * [verify_openid_openkey](/bkapi/verify_openid_openkey/)：检查 `openid` 和 `openkey` 是否有效
    * [get_auth_token](/bkapi/get_auth_token/)：通过用户的 `openid` 和 `openkey` 获取用户的 `auth_token`（`auth_token` 似乎和 `access_token` 是相同的，这个 API 的功能似乎和 `get_user_access_token` 是相同的，但是这个可以从公网访问）

* 通知组件 API

    * [send_email](/bkapi/send_email/)：向指定的邮箱、`uin` 或 `openid` 发送邮件
    * [send_sms](/bkapi/send_sms/)：向指定的手机号、`uin` 或 `openid` 发送短信
