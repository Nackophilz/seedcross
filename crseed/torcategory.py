import re
import os


def cutExt(torName):
    if not torName:
        return ''
    tortup = os.path.splitext(torName)
    torext = tortup[1].lower()
    if re.match(r'\.[0-9a-z]{2,8}$', torext, flags=re.I):
    # mvext = ['.mkv', '.ts', '.m2ts', '.vob', '.mpg', '.mp4', '.3gp', '.mov', '.tp', '.zip', '.pdf', '.iso', '.ass', '.srt', '.7z', '.rar']
    # if torext.lower() in mvext:
        return tortup[0].strip()
    else:
        return torName

class CategoryItem:
    def __init__(label, number):
        label = label
        number = number
        # size = 0


class GuessCategoryUtils:
    # def __init__(self):
    # Some groups produce TV Series but don't display S01 in the torrent name
    TV_GROUPS = ['CMCTV', 'FLTTH']
    WEB_GROUPS = ['CHDWEB', 'PTerWEB', 'HaresWEB', 'DBTV', 'QHStudio', 
                 'LeagueWEB', 'HDCTV', '52KHD', 'PTHweb', 'OURTV', 'iLoveTV']

    # Some groups specifically produce MV
    MV_GROUPS = ['PTerMV', 'FHDMv', 'Melon', 'HaresMV', 'Bugs!']
    # Some groups specifically produce Audio
    AUDIO_GROUPS = ['PTHAudio', 'HDSAB']
    # Some groups specifically do encoding but don't mark it in the torrent name
    MOVIE_ENCODE_GROUPS = ['CMCT', 'FRDS']

    CATEGORIES = {
        'TV': ['TV', '32', 0, 'TV'],
        'MV': ['MV', '31;1', 0, 'MV'],
        'Audio': ['Audio', '32;1', 0, 'Audio'],
        'Music': ['Music', '31', 0, 'Music'],
        'eBook': ['eBook', '34', 0, 'eBook'],
        # Encode 1080p and lower, suitable for emby
        'MovieEncode': ['MovieEncode', '36', 0, 'MovieEncode'],
        # Remux 1080p and lower, suitable for emby
        'MovieRemux': ['MovieRemux', '36', 0, 'MovieRemux'],
        'Movie4K': ['Movie4K', '36', 0, 'Movie4K'],  # Encode and Remux 4K, suitable for emby
        'MovieWebdl': ['MovieWebdl', '36', 0, 'MovieWebdl'],  # Web DL, suitable for emby
        'MovieWeb4K': ['MovieWeb4K', '36', 0, 'MovieWeb4K'],  # Web DL, suitable for emby
        # Original disk, suitable for player & kodi
        'MovieBDMV': ['MovieBDMV', '35', 0, 'MovieBDMV'],  # Original disk, suitable for player & kodi
        'MovieBDMV4K': ['MovieBDMV4K', '35', 0, 'MovieBDMV4K'],
        'MovieDVD': ['MovieDVD', '35', 0, 'MovieDVD'],
        'Movie': ['Movie', '35', 0, 'Movie'],
        'HDTV': ['HDTV', '33', 0, 'HDTV'],
        'Other': ['Other', '33', 0, 'Others']
    }

    category = ''
    group = ''
    resolution = ''
    quality = ''
    CategorySummary = []

    def setCategory(self, category):
        self.category = category
        self.CATEGORIES[category][2] += 1

    def categoryByExt(self, torName):
        if re.search(
                r'(pdf|epub|mobi|txt|chm|azw3|CatEDU|eBook-\w{4,8}|mobi|doc|docx).?$',
                torName, re.I):
            self.setCategory('eBook')
        elif re.search(
                r'(zip|7z|rar).?$',
                torName, re.I):
            self.setCategory('Other')
        elif re.search(r'\.(mpg)\b', torName, re.I):
            self.setCategory('MV')
        elif re.search(r'(\b|_)(FLAC.{0,3}|DSF.{0,3}|DSD(\d{1,3})?)$', torName, re.I):
            self.setCategory('Music')
        elif re.search(r'(\b|_)(BD25\b|BD50\b|BD66\b|BD$)', torName, re.I):
            self.setCategory('MovieBDMV')
        elif re.search(r'(\b|_)(DVDR|DVD(\d+)?)\b', torName, re.I):
            self.setCategory('MovieDVD')
        else:
            return False
        return True

    def categoryByKeyword(self, torName):
        if re.search(r'(PDF|epub|mobi|txt|azw3)', torName, re.I):
            self.setCategory('eBook')
        elif re.search(r'(\bConcert|\bLive[. ](At|in))\b', torName, re.A | re.I):
            self.setCategory('MV')
        elif re.search(r'\bBugs!.?\.mp4', torName, re.I):
            self.setCategory('MV')
        elif re.search(r'(\bVarious Artists|\bMQA\b|\bLPCD|\bSACD|\bMP3|XRCD\d{1,3})',
                       torName, re.A | re.I):
            self.setCategory('Music')
        elif re.search(r'(\b\d+ ?CD|(\[|\()\s*(16|24)\b|\-(44\.1|88.2|48|192)|24Bit|44\s*\]|FLAC.*(16|24|48|CUE|WEB|Album)|WAV.*CUE|CD.*FLAC|(\[|\()\s*FLAC)', torName, re.A | re.I):
        # elif re.search(r'(\b\d+ ?CD|24\-|\-44\.1|24Bit|\[[\d\s]*44\s*\]|FLAC.*44|FLAC.*48|WAV.*CUE|FLAC.*CUE|\[.*FLAC\]|FLAC.+WEB\b|FLAC.*Album|CD[\s-]+FLAC|FLAC[\s-]+CD)', torName, re.A | re.I):
            self.setCategory('Music')
        elif re.search(r'^(Beethoven|Schubert)\s*[\-_]', torName, re.I):
            self.setCategory('Music')
        elif re.search(r'(Symphony|Concerto|Sonata|Quartet|Trio|Album\b)', torName, re.I):
            self.setCategory('Music')
        elif re.search(r'(\[BDMV\])', torName, re.I):
            self.setCategory('MovieBDMV')
        elif re.search(r'(\bThe.Movie.\d{4})\b', torName, flags=re.A | re.I):
            if self.quality == 'WEBDL':
                self.setCategory('MovieWebdl')
            else:
                self.setCategory('MovieEncode')
        else:
            return False
        return True

    def categoryTvByName(self, torName):
        if re.search(r'(\b(S\d+)(E\d+)?|(Ep?\d+-Ep?\d+))\b', torName, flags=re.A | re.I):
            self.setCategory('TV')
        elif re.search(r'(\bS\d+(-S\d+))\b', torName, flags=re.A | re.I):
            self.setCategory('TV')
        elif re.search(r'\W[ES]\d+\W|EP\d+\W', torName, re.A | re.I):
            self.setCategory('TV')
        elif re.search(r'\bHDTV\b', torName):
            self.setCategory('HDTV')
        elif re.search(r'Complete.+Web-?dl|Full.Season', torName, re.A | re.I):
            self.setCategory('TV')
        else:
            return False
        return True

    def categoryMVAudioGroup(self, torName, group):
        if group in self.MV_GROUPS:
            self.setCategory('MV')
        elif group in self.AUDIO_GROUPS:
            self.setCategory('Audio')
        else:
            return False
        return True


    def categoryByGuessGroup(self, torName, group):
        filename, file_ext = os.path.splitext(torName)
        isMediaFile = file_ext.lower() in ['.mkv', '.mp4', '.iso']
            
        if group in self.TV_GROUPS and not isMediaFile:
            self.setCategory('TV')
        elif group in self.WEB_GROUPS and not isMediaFile:
            self.setCategory('TV')
        elif group in self.MOVIE_ENCODE_GROUPS:
            self.setCategory('MovieEncode')
        else:
            return False
        return True


    def parseGroup(self, torName):
        sstr = cutExt(torName)
        match = re.search(r'[@\-￡]\s?(\w+)(?!.*[@\-￡].*)$', sstr, re.I)
        if match:
            groupName = match.group(1).strip()
            # # TODO: BD-50_A_PORTRAIT_OF_SHUNKIN_1976_BC
            if match.span(1)[0] < 4:
                return None
            if groupName.startswith('CMCT') and not groupName.startswith('CMCTV'):
                groupName = 'CMCT'
            return groupName

        return None

    def getResolution(self, torName):
        match = re.search(r'\b(2160p|1080[pi]|720p|576p|480p)\b', torName, re.A | re.I)
        if match:
            return match.group(0).strip().lower()
        else:
            return ''

    def getSource(self, torName):
        match = re.search(r'\b(Blu[\-\. ]?Ray|WEB|WEB[\-\. ]?DL|WEBRip|^BD([-. ]\d)*|BD$)\b', torName, re.A | re.I)
        if match:
            # mediaSource = match.group(0).strip().lower()
            if re.search(r'(\bBlu|\bBD)', match.group(0), flags=re.A | re.I):
                return 'BLURAY'
            else:
                return 'WEBDL'
        else:
            return ''

    def categoryByQuality(self, torName):
        # Source is Original Disk
        if self.quality == 'BLURAY':
            # Remux, Encode or Original Disk
            if re.search(r'\WREMUX\W', torName, re.I):
                # if self.resolution == '2160p':
                #     self.setCategory('Movie4K')
                # else:
                #     self.setCategory('MovieRemux')
                self.setCategory('MovieRemux')
            elif re.search(r'\b(x265|x264)\b', torName, re.I):
                # if self.resolution == '2160p':
                #     self.setCategory('Movie4K')
                # else:
                #     self.setCategory('MovieEncode')
                self.setCategory('MovieEncode')
            else:
                if self.resolution == '2160p':
                    self.setCategory('MovieBDMV4K')
                else:
                    self.setCategory('MovieBDMV')
        # Source is WEB-DL
        elif self.quality == 'WEBDL': 
            # if self.resolution == '2160p':
            #     self.setCategory('MovieWeb4K')
            # else:
            #     self.setCategory('MovieWebdl')
            self.setCategory('MovieWebdl')
        else:
            if re.search(r'\WREMUX\W', torName, re.I):
                self.setCategory('MovieRemux')
            elif re.search(r'\b(x265|x264)\b', torName, re.I):
                self.setCategory('MovieEncode')
            else:
                return False
        return True

    def guessByName(self, torName):
        self.group = self.parseGroup(torName)
        self.quality = self.getSource(torName)
        self.resolution = self.getResolution(torName)

        if self.categoryMVAudioGroup(torName, self.group):
            return self.category, self.group

        if self.categoryByExt(torName):
            return self.category, self.group

        if self.categoryTvByName(torName):
            return self.category, self.group

        if self.categoryByKeyword(torName):
            return self.category, self.group

        if self.categoryByGuessGroup(torName, self.group):
            return self.category, self.group

        # Not produced by web groups
        if self.categoryByQuality(torName):
            return self.category, self.group
        else:
            if self.resolution or self.quality:
                self.setCategory('Movie')
            else:
                # Other condition: TV/MV/Audio don't match, quality not marked, encode groups don't match
                self.setCategory('Other')
            return self.category, self.group

    def getSummary(self):
        for cat in self.CATEGORIES.keys():
            ic = CategoryItem(self.CATEGORIES[cat][0],
                              self.CATEGORIES[cat][2])
            self.CategorySummary.append(ic)
        return self.CategorySummary
