#!/usr/bin/env fish

for log in "#urlab" "#urlab35c3" "#titoufaitdestests" "#ci"
    scp ititou.be:.weechat/logs/irc.freenode.$log.weechatlog feeder/irclogs/$log.weechat
end
