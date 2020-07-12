from Components.Converter.Converter import Converter
from os import statvfs, environ
from Components.Element import cached, ElementError
from Poll import Poll
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from Components.Language import language
import gettext

lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("SevenHD", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/SevenHD/locale/"))

def _(txt):
    t = gettext.dgettext("SevenHD", txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t

class speedyHDDiskSpace(Poll, Converter, object):
    free = 0
    size = 1
    both = 2
    path = 3

    def __init__(self, type):
        Converter.__init__(self, type)
        Poll.__init__(self)
        if type == "free":
            self.type = self.free
        elif type == "size":
            self.type = self.size
        elif type == "both":
            self.type = self.both
        elif type == "path":
            self.type = self.path

        self.poll_interval = 2000
        self.poll_enabled = True

    @cached
    def getText(self):
        service = self.source.service
        if service:
            if self.type == self.free:
                try:
                    stat = statvfs(service.getPath().replace('Latest Recordings', ''))
                    hdd = stat.f_bfree * stat.f_bsize
                    if hdd > 1099511627776:
                        free = float(hdd/1099511627776.0)
                        return '%.2f TB' % free
                    elif hdd > 1073741824:
                        free = float(hdd/1073741824.0)
                        return '%.2f GB' % free
                    elif hdd > 1048576:
                        free = float(hdd/1048576.0)
                        return '%i MB' % free
                except OSError:
                    return 'N/A'

            elif self.type == self.size:
                try:
                    stat = statvfs(service.getPath().replace('Latest Recordings', ''))
                    hddsize = stat.f_blocks * stat.f_bsize
                    if hddsize > 1099511627776:
                        locks = float(hddsize/1099511627776.0)
                        return '(%.2f TB)' % locks
                    elif hddsize > 1073741824:
                        locks = float(hddsize/1073741824.0)
                        return '(%.2f GB)' % locks
                    elif hddsize > 1048576:
                        locks = float(hddsize/1048576.0)
                        return '(%i MB)' % locks
                except OSError:
                    return 'N/A'

            elif self.type == self.both:
                try:
                    stat = statvfs(service.getPath().replace('Latest Recordings', ''))
                    hdd = stat.f_bfree * stat.f_bsize
                    hddsize = stat.f_blocks * stat.f_bsize
                    if hdd > 1099511627776:
                        free = float(hdd/1099511627776.0)
                        locks = float(hddsize/1099511627776.0)
                        return ('%.2f TB' % locks) + (', %.2f TB (' % free) + str((100 * stat.f_bavail) // stat.f_blocks) + '%) ' + _('free')
                    elif hdd > 1073741824:
                        free = float(hdd/1073741824.0)
                        locks = float(hddsize/1073741824.0)
                        return ('%.2f GB' % locks) + (', %.2f GB (' % free) + str((100 * stat.f_bavail) // stat.f_blocks) + '%) ' + _('free')
                    elif hdd > 1048576:
                        free = float(hdd/1048576.0)
                        locks = float(hddsize/1048576.0)
                        return ('%i MB' % locks) + (', %i MB (' % free) + str((100 * stat.f_bavail) // stat.f_blocks) + '%) ' + _('free')
                except OSError:
                    return 'N/A'

            elif self.type == self.path:
                if "." in str(service.getPath()) or "@" in str(service.getPath()) or "Latest Recordings" in str(service.getPath()):
                    return service.getPath().rsplit('/', 1)[0]
                else:
                    return service.getPath().replace('/Latest Recordings', '')

        return ""

    text = property(getText)

    def changed(self, what):
        if what[0] is self.CHANGED_SPECIFIC:
            Converter.changed(self, what)
        elif what[0] is self.CHANGED_POLL:
            self.downstream_elements.changed(what)
