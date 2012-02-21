from ..compat import getModule as _
for i,j in _("urllib").__dict__.items():
    locals()[i]=j;