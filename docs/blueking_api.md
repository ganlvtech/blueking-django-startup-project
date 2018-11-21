* 内部 OAuth API（仅能在服务器内部网络访问）

    * [get_app_access_token](/bkapi/get_app_access_token/)：获取代表应用权限的 `access_token`
    * [get_user_access_token](/bkapi/get_user_access_token/)：通过用户的 `openid` 和 `openkey` 获取用户的 `access_token`（包括 `refresh_token`）
    * [refresh_user_access_token](/bkapi/refresh_user_access_token/)：通过 `refresh_token` 重新获取获取用户的 `access_token`

* 获取用户信息 API

    * [get_user_info](/bkapi/get_user_info/)：通过用户的 `openid` 和 `openkey` 获取用户 QQ 号和头像
    * [get_openid_openkey](/bkapi/get_openid_openkey/)：通过 Cookie 中的 `uin` 和 `skey` 获取用户的 `openid` 和 `openkey`
    * [verify_openid_openkey](/bkapi/verify_openid_openkey/)：检查 `openid` 和 `openkey` 是否有效
    * [get_auth_token](/bkapi/get_auth_token/)：通过用户的 `openid` 和 `openkey` 获取用户的 `auth_token`（似乎和 `access_token` 是一个东西，但是这个 API 可以从公网访问）

* 通知组件 API

    * [send_email](/bkapi/send_email/)：向指定的邮箱、`uin` 或 `openid` 发送邮件
    * [send_sms](/bkapi/send_sms/)：向指定的手机号、`uin` 或 `openid` 发送短信
