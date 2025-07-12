import gi
gi.require_version('IBus', '1.0')
from gi.repository import IBus
from gi.repository import GLib
from time import sleep

class PressBackspace:
    def __init__(self, engine):
        self.engine = engine
    def exec(self, count):
        for _ in range(count):
            self.engine.forward_key_event(
                IBus.keyval_from_name('BackSpace'),
                14,
                0
            )
            self.engine.forward_key_event(
                IBus.keyval_from_name('BackSpace'),
                14,
                IBus.ModifierType.RELEASE_MASK
            )

class UnicodeEngine(IBus.EngineSimple):
    def __init__(self, bus, object_path):
        self.name = "bijoy:unicode"
        if hasattr(IBus.Engine.props, 'has_focus_id'):
            super(UnicodeEngine, self).__init__(engine_name= self.name,
                                         connection=bus.get_connection(),
                                         object_path=object_path)
        else:
            super(UnicodeEngine, self).__init__(engine_name=self.name,
                                         connection=bus.get_connection(),
                                         object_path=object_path)
        #self.active_surrounding_text =True
        self.connect('process-key-event', self.process_key_event)
        self.connect('focus-in', lambda x: self.clean_context())
        self.pressback = PressBackspace(self)
        #self.connect('set-cursor-location', self.clean_context)
        
        self.map = {33: '!', 34: '”', 35: '#', 36: '৳', 37: '%', 38: 'ঁ', 39: '’', 40: '(', 41: ')', 42: '*', 45: '-', 48: '০', 49: '১', 50: '২', 51: '৩', 52: '৪', 53: '৫', 54: '৬', 55: '৭', 56: '৮', 57: '৯', 64: '@', 65: 'র্', 66: 'ণ', 67: 'ৈ', 68: 'ী', 69: 'ঢ', 70: 'অ', 71: '।', 72: 'ভ', 73: 'ঞ', 74: 'খ', 75: 'থ', 76: 'ধ', 77: 'শ', 78: 'ষ', 79: 'ঘ', 80: 'ঢ়', 81: 'ং', 82: 'ফ', 83: 'ূ', 84: 'ঠ', 85: 'ঝ', 86: 'ল', 87: 'য়', 88: 'ৗ', 89: 'ছ', 90: '\u200d্য', 92: 'ৎ', 94: '\u09b3', 95: '_', 96: '‘', 97: 'ৃ', 98: 'ন', 99: 'ে', 100: 'ি', 101: 'ড', 102: 'া', 103: '্', 104: 'ব', 105: 'হ', 106: 'ক', 107: 'ত', 108: 'দ', 109: 'ম', 110: 'স', 111: 'গ', 112: 'ড়', 113: 'ঙ', 114: 'প', 115: 'ু', 116: 'ট', 117: 'জ', 118: 'র', 119: 'য', 120: 'ও', 121: 'চ', 122: '্র', 124: 'ঃ', 126: '“', 65456: '০', 65457: '১', 65458: '২', 65459: '৩', 65460: '৪', 65461: '৫', 65462: '৬', 65463: '৭', 65464: '৮', 65465: '৯'}
        self.rep = [{'্ি': 'ই', '্ী': 'ঈ', '্ু': 'উ', '্ূ': 'ঊ', '্ৃ': 'ঋ', '্ে': 'এ', '্ৈ': 'ঐ', '্ৗ': 'ঔ', 'ৌ': 'ৌ', 'ো': 'ো', '্া': 'আ', 'অা': 'আ', 'ঁা': 'াঁ', 'ঁু': 'ুঁ', 'ঁূ': 'ূঁ', 'ঁৃ': 'ৃঁ', '্্': '্\u200c', 'েো': ' ো', 'েৌ': 'ৌ', ' ু': ' \u200dু', ' ূ': ' \u200dূ', ' ৃ': ' \u200dৃ', ' ”': ' “', ' ’': ' ‘'}, {'েঁৗ': 'ৌঁ', 'েঁা': 'োঁ', 'ু্র': '্রু', 'ু্য': '্যু', 'ূ্র': '্রূ', 'ূ্য': '্যূ', 'ৃ্র': '্রৃ', 'ৃ্য': '্যৃ'}]
        self.rep_ki = [['ে', 'অ', ' ', '্', 'ঁ'],['ে', 'ূ', 'ৃ', 'ু']]
        self.bef =['ে','ৈ','ি']
        self.context = ""  # Track previous characters/state
        self.preedit = ""  # Temporary preedit buffer
        
    def get_char(self, input):
      return self.map.get(input, False)
  
    def update_preedit(self, preedit):
        # Update the preedit text in the application
        text = IBus.Text.new_from_string(preedit)
        self.update_preedit_text(text, len(preedit), True)

    def send_backspace(self, count):
        # Simulate backspace presses (limited to IBus's capabilities)
        self.pressback.exec(count)
    def clean_context(self):
        self.context = ""
    
    def process_key_event(self, obj, keyval, keycode, state):
                      
        if state not in [16, 17, 0, 1]: #Blocking keyup events and enabling Gnome search writing 
            return False
            
        if keycode in [103, 105, 106, 108, 102, 107, 104, 109]: #Pressing Arrows
            self.clean_context()
            return False  
        char = self.get_char(keyval) #Lookup Table
        
        if not char and keycode == 14: #If not a return from char then..
            if self.context: self.context = self.context[:-1]
            if self.preedit:
                self.preedit = ""
                self.update_preedit("")
            return False
        elif not char and keyval ==32:
          self.context = " "
          return False
        elif not char:
            return False  # Let IBus handle the key normally
        
        #Important Swaping Here
        if char in self.bef and not (self.context and self.context[-1]=='্'):
          self.preedit = char
          self.update_preedit(char)
          return True
        elif char == '্' and self.context and self.context[-1] in self.bef:
          self.preedit = self.context[-1]
          self.send_backspace(1)
          self.commit_text(IBus.Text.new_from_string(char))
          self.context = self.context[0] +'্'
          self.update_preedit(self.preedit)
          return True
        
        #elif keyval==65 and :
        elif keyval==65: #A
          self.send_backspace(len(self.context))
          char += self.context
          self.context = self.context[:-1]
          self.commit_text(IBus.Text.new_from_string(char))
          return True
        elif (keyval==122 or keyval==90) and self.context and (self.context[-1] in self.bef or self.context[-1] in ['ৌ', 'ো'] ):
          self.send_backspace(1)
          char += self.context[-1]
          self.context = self.context[:-1]
          self.commit_text(IBus.Text.new_from_string(char))
          return True
        
        # Preparing the Context for later inputs...
        if self.preedit:
          self.update_preedit("") 
          if self.context and self.context[-1] == '্':
            self.context += char+self.preedit
            char = char+self.preedit
          else:
            self.context = char+self.preedit
            char = self.context
          self.preedit = "" # Protecting context from distroying
        elif not self.context:
            self.context = char
        elif self.context[-1] in self.rep_ki[0]:
          context = self.context
          self.context = self.rep[0].get(self.context[-1]+char, char)
          if self.context != char:
            char = self.context
            if not context[-1] == " ": self.send_backspace(1)                
            else: char = char[-1]
          elif context[-1] == '্':
            self.context +=char
        elif self.context[-1] == '্':
            self.context = context+char
        elif char == '্':
            self.context += char
        elif len(self.context)<2 and self.context[0] == self.rep_ki[1]:
            self.context += char
        elif self.context[0] in self.rep_ki[1] and (self.context+char) in self.rep[1]:
            char = self.rep[1][self.context+char]
            self.send_backspace(len(self.context))
            self.context = char[-1]
        else:
            self.context = char[-1]
            
        self.commit_text(IBus.Text.new_from_string(char))
        return True  # Key event handled


class ClassicEngine(IBus.EngineSimple):
    def __init__(self, bus, object_path):
        self.name = "bijoy:classic"
        if hasattr(IBus.Engine.props, 'has_focus_id'):
            super(ClassicEngine, self).__init__(engine_name= self.name,
                                         connection=bus.get_connection(),
                                         object_path=object_path)
        else:
            super(ClassicEngine, self).__init__(engine_name=self.name,
                                         connection=bus.get_connection(),
                                         object_path=object_path)
        #self.active_surrounding_text =True
        self.connect('process-key-event', self.process_key_event)
        self.connect('focus-in', lambda x: self.clean_context())
        #self.connect('set-cursor-location', self.clean_context)
        print('Engine initialized...')
        self.pressback = PressBackspace(self)
        self.context=""
        self.preedit=""
        self.map = {34: 'Ó', 38: 'u', 39: 'Õ', 45: '-', 55: '7', 65: '©', 66: 'Y', 67: '‰', 68: 'x', 69: 'X', 70: 'A', 71: '|', 72: 'f', 73: 'T', 74: 'L', 75: '_', 76: 'a', 77: 'k', 78: 'l', 79: 'N', 80: 'p', 81: 's', 82: 'd', 83: '~', 84: 'V', 85: 'S', 86: 'j', 87: 'q', 88: 'Š', 89: 'Q', 90: '¨', 92: 'r', 95: 'Ñ', 96: 'Ô', 97: '„', 98: 'b', 99: '‡', 100: 'w', 101: 'W', 102: 'v', 103: '&', 104: 'e', 105: 'n', 106: 'K', 107: 'Z', 108: '`', 109: 'g', 110: 'm', 111: 'M', 112: 'o', 113: 'O', 114: 'c', 115: 'y', 116: 'U', 117: 'R', 118: 'i', 119: 'h', 120: 'I', 121: 'P', 122: 'ª', 124: 't', 126: 'Ò'}
        self.rep = [{'&v': 'Av', '&i': 'ª', '&w': 'B', '&x': 'C', '&y': 'D', '&~': 'E', '&„': 'F', '&‡': 'G', ' ‡': ' †', '&‰': 'H', ' ‰': ' ˆ', '&Š': 'J', 'Ky': 'Kz', 'K~': 'K‚', 'K„': 'K…', '°y': '°z', '°~': '°‚', '°„': '°…', '³ª': '³«', '±y': '±z', '±~': '±‚', '±„': '±…', 'Kª': 'µ', 'µy': 'µz', 'µ~': 'µ‚', 'µ„': 'µ…', 'ÿy': 'ÿz', 'ÿ~': 'ÿ‚‚', 'ÿ„': 'ÿ…', '³y': '³z', '³~': '³‚', '³„': '³…', 'My': '¸', '»y': '»z', '»~': '»‚', '»„': '»…', 'Mª': 'MÖ', 'Oy': 'Oz', 'O~': 'O‚', 'O„': 'O…', '¼y': '¼z', '¼~': '¼‚', '¼„': '¼…', '¼ª': '¼«', 'Py': 'Pz', 'P~': 'P‚', 'P„': 'P…', 'Qy': 'Qz', 'Q~': 'Q‚', 'Q„': 'Q…', 'Qª': 'Q«', 'Àz': 'Àz', 'À~': 'À‚', 'À„': 'À…', 'Áy': 'Áz', 'Á~': 'Á‚', 'Á„': 'Á…', 'Sy': 'Sz', 'S~': 'S‚', 'S„': 'S…', 'Ty': 'Tz', 'T~': 'T‚', 'T„': 'T…', 'Ây': 'Âz', 'Â‚': 'Â‚', 'Â…': 'Â…', 'Ãy': 'Ãz', 'Ã~': 'Ã‚', 'Ã„': 'Ã…', 'Uy': 'Uz', 'U~': 'U‚', 'U„': 'U…', 'Æy': 'Æz', 'Æ~': 'Æ‚', 'Æ„': 'Æ…', 'Vy': 'Vz', 'V~': 'V‚', 'V„': 'V…', 'Wy': 'Wz', 'W~': 'W‚', 'W„': 'W…', 'Çy': 'Çz', 'Ç~': 'Ç‚', 'Ç„': 'Ç…', 'Xy': 'Xz', 'X~': 'X‚', 'X„': 'X…', 'Èy': 'Èz', 'È~': 'È‚', 'È„': 'È…', 'Éy': 'Éz', 'É~': 'É‚', 'É„': 'É…', 'Ðy': 'Ðz', 'Ð~': 'Ð‚', 'Ð„': 'Ð…', 'Zy': 'Zz', 'Z~': 'Z‚', 'Z„': 'Z…', 'Ëy': 'Ëz', 'Ë~': 'Ë‚', 'Ë„': 'Ë…', 'Zª': 'Î', 'Îy': 'Îæ', 'Î~': 'Îƒ', '×y': '×z', '×~': '×‚', '×„': '×…', 'Ûy': 'Ûz', 'Û~': 'Û‚', 'Û„': 'Û…', 'Úy': 'Úz', 'Ú~': 'Ú‚', 'Ú„': 'Ú…', 'Üy': 'Üz', 'Ü~': 'Ü‚', 'Ü„': 'Ü…', 'Üª': 'Ü«', 'ßy': 'ßz', 'ß~': 'ß‚', 'ß„': 'ß…', 'Þy': 'Þz', 'Þ~': 'Þ‚', 'Þ„': 'Þ…', 'cª': 'cÖ', 'dy': 'dz', 'd~': 'd‚', 'd„': 'd…', 'dª': 'd«', '&.': 'ž', 'äy': 'äz', 'ä~': 'ä‚', 'ä„': 'ä…', 'fy': 'fz', 'f~': 'f‚', 'f„': 'f…', 'fª': 'å', 'åy': 'åæ', 'å~': 'åƒ', 'çy': 'çz', 'ç~': 'ç‚', 'ç„': 'ç…', 'gª': '¤ª', 'iy': 'iæ', 'i~': 'iƒ', 'éy': 'éz', 'é~': 'é‚', 'é„': 'é…', 'îy': 'îz', 'î~': 'î~', 'î„': 'î…', 'îª': 'î«', 'ky': 'ï', 'kª': 'kÖ', 'ðy': 'ðz', 'ð~': 'ð‚', 'ð„': 'ð…', 'ñy': 'ñz', 'ñ~': 'ñ‚', 'ñ„': 'ñ…', 'óy': 'óz', 'ó~': 'ó‚', 'ó„': 'ó…', 'ôy': 'ôz', 'ô~': 'ô‚', 'ô„': 'ô…', 'õy': 'õz', 'õ~': 'õ‚', 'õ„': 'õ…', 'òy': 'òz', 'ò~': 'ò‚', 'ò„': 'ò…', 'mª': '¯ª', 'ùy': 'ùz', 'ù~': 'ù‚', 'ù„': 'ù…', 'ùª': 'ù«', 'ny': 'û', 'n„': 'ü', 'þy': 'þz', 'þ~': 'þ~', 'þ„': 'þ„', 'nª': 'n«', 'oy': 'o–', '&|': '\\', '&e': '¦', '&j': 'ø', '&g': '¥', '&b': 'œ', '&Z': 'Í', '&;': 'Ê', '&Ô': '“', '÷y': '÷z', '÷~': '÷‚‚', '÷„': '÷…', 'ëy': 'ëz', 'ë~': 'ë‚‚', 'ë„': 'ë…'}, {'K&K': '°', 'K&U': '±', 'K&b': 'Kè', 'Kèy': 'Kèz', 'Kè~': 'Kè‚', 'Kè„': 'Kè…', 'K&e': 'K¡', 'K&g': '´', 'K&j': 'K¬', 'K¬y': 'K¬z', 'K¬~': 'K¬‚', 'K¬„': 'K¬…', 'ÿ&g': '²', 'K&l': 'ÿ', 'K&m': '·', 'K&Z': '³', 'ÿ&b': 'ÿè', 'ÿèy': 'ÿèz', 'ÿè~': 'ÿè‚', 'ÿè„': 'ÿè…', 'Lªy': 'Lªæ', 'Lª~': 'Lªƒ', 'O&M': '½', 'M&`': 'º', 'M&a': '»', 'M&b': 'Mœ', 'M&g': 'M¥', 'M&j': 'Mø', 'MÖy': 'MÖæ', 'MÖ~': 'MÖƒ', 'M&e': 'M¦', 'N&b': 'Nœ', 'Nªy': 'Nªæ', 'Nª~': 'Nªƒ', 'O&K': '¼', 'O&L': '•L', 'O&N': '•N', 'O&g': '•g', '¼«y': '¼«z', '¼«~': '¼«‚', '¼«„': '¼«…', '¼&l': '•ÿ', '•ÿy': '•ÿz', '•ÿ~': '•ÿ‚', '•ÿ„': '•ÿ…', 'P&P': '”P', '”Py': '”Pz', '”P~': '”P‚', '”P„': '”P…', 'P&Q': '”Q', '”Qy': '”Qz', '”Q~': '”Q‚', '”Q„': '”Q…', '”Qª': '”Q«', 'P&T': '”T', '”Ty': '”Tz', '”T~': '”T‚', '”T„': '”T…', 'R&R': '¾', 'R&S': 'À', 'R&T': 'Á', 'R&e': 'R¦', '¾&e': '¾¡', 'T&P': 'Â', 'T&Q': 'Ã', 'T&R': 'Ä', 'T&S': 'Å', 'U&U': 'Æ', 'U&e': 'U¡', 'U&g': 'U¥', 'W&W': 'Ç', 'Y&U': 'È', 'Y&V': 'É', 'Y&W': 'Ð', 'Y&b': 'Yœ', 'Y&e': 'Y¦', 'Z&Z': 'Ë', 'Z&_': 'Ì', 'Z&b': 'Zœ', 'Z&e': 'Z¡', 'Z&g': 'Z¥', 'Ë&e': 'Ë¡', '_&e': '_¡', '`&M': '˜M', '`&N': '˜N', '`&`': 'Ï', '`&a': '×', '`&f': '™¢', '™¢y': '™¢z', '™¢~': '™¢‚', '™¢„': '™¢…', '`&e': 'Ø', '`&g': 'Ù', '™¢ª': '™£', '™£y': '™£æ', '™£~': '™£ƒ', 'a&e': 'aŸ', '`ªy': '`ªæ', '`ª~': '`ªƒ', 'a&g': 'a¥', 'aªy': 'aªæ', 'aª~': 'aªƒ', 'b&U': '›U', '›Uy': '›Uz', '›U~': '›U‚', '›U„': '›U…', 'b&W': 'Û', 'b&V': 'Ú', 'b&Z': 'šÍ', 'šÍy': 'š‘', 'šÍ~': 'šÍ‚', 'šÍ„': 'šÍ…', 'b&_': 'š’', 'š’y': 'š’z', 'š’~': 'š’‚', 'š’„': 'š’…', 'b&`': '›`', 'b&a': 'Ü', 'b&b': 'bœ', 'b&e': 'š^', 'b&g': 'b¥', 'šÍª': 'š¿', 'Ü«y': 'Ü«z', 'Ü«~': 'Ü«‚', 'Ü«„': 'Ü«…', 'b&m': 'Ý', 'c&Z': 'ß', 'c&U': 'Þ', 'c&c': 'à', 'c&j': 'cø', 'c&b': 'cœ', 'cÖy': 'cÖæ', 'cÖ~': 'cÖƒ', 'd«y': 'd«z', 'd«~': 'd«‚', 'd«„': 'd«…', 'd&j': 'd¬', 'd¬y': 'd¬z', 'd¬~': 'd¬‚', 'd¬„': 'd¬„', 'e&R': 'â', 'e&j': 'eø', 'e&`': 'ã', 'e&a': 'ä', 'e&e': 'eŸ', 'eªy': 'eªæ', 'eª~': 'eªƒ', 'f&j': 'fø', 'g&b': '¤œ', 'g&j': '¤ø', 'g&c': '¤ú', 'g&d': 'ç', 'g&e': '¤^', 'g&f': '¤¢', '¤¢ª': '¤£', 'g&g': '¤§', 'j&K': 'é', 'j&W': 'ì', 'j&c': 'í', 'j&d': 'î', 'j&e': 'j¦', 'j&g': 'j¥', 'j&j': 'jø', 'kÖy': 'kÖæ', 'kÖ~': 'kÖƒ', 'k&P': 'ð', 'k&Q': 'ñ', 'k&b': 'kœ', 'k&e': 'k^', 'k&g': 'k¥', 'l&K': '®‹', '®‹y': '®‹z', '®‹~': '®‹‚', '®‹„': '®‹…', 'l&U': 'ó', 'l&V': 'ô', 'l&c': '®ú', '®úª': '®úÖ', 'l&d': 'õ', '®‹ª': '®Œ', '®Œy': '®Œz', '®Œ~': '®Œ‚', '®Œ„': '®Œ„', 'l&Y': 'ò', 'l&g': '®§', 'm&K': '¯‹', '¯‹y': '¯‹z', '¯‹~': '¯‹‚', '¯‹„': '¯‹…', 'm&L': 'ö', 'm&Z': '¯Í', '¯Íy': '¯‘', '¯Í~': '¯Í‚', '¯Í„': '¯Í…', 'm&_': '¯’', '¯’y': '¯’z', '¯’~': '¯’‚', '¯’„': '¯’…', 'm&j': '¯ø', 'm&c': '¯ú', 'm&e': '¯^', 'm&d': 'ù', 'ù«y': 'ù«z', 'ù«~': 'ù«‚', '¯Íª': '¯¿', 'm&b': '¯œ', 'm&g': '¯§', '¯‹ª': '¯Œ', '¯Œy': '¯Œz', '¯Œ~': '¯Œ‚', '¯Œ„': '¯Œ…', 'n&Y': 'nè', 'n&b': 'ý', 'n&e': 'nŸ', 'n&g': 'þ', 'n&j': 'n¬', 'm&U': '÷', 'j&U': 'ë', 'j&M': 'ê', 'c&m': 'á', 'M&M': '¹'}, {'”Q&e': '”Q¡', '˜M&y': '`&¸', '›`&e': '›Ø', '›`ªy': '›`ªæ', '›`ª~': '›`ªƒ', '¤ú&j': '¤úø', '(A)i': '(A)i', '®úªy': '®úÖæ', '®úª~': '®úÖƒ', '¯Í&e': '¯Í¡', '¯‹&j': '¯‹¬', '¯‹¬y': '¯‹¬z', '¯ú&j': '¯úø', 'n&e2': 'n¡', 'šÍ&e': 'šÍ¡'}] 
        self.rep_ki=[['ó', 'P', 'K', 'i', 'f', 'n', '±', '³', 'ô', 'd', 'W', 'ÿ', 'Ë', 'Û', 'ë', '¼', 'Q', 'ò', 'þ', '÷', 'É', 'Ü', 'ç', '°', ' ', 'õ', 'å', 'k', 'O', 'ß', 'T', 'U', 'Z', 'Á', 'Ã', 'Ú', 'ä', 'À', 'Î', 'Æ', 'X', 'o', '&', 'î', 'S', 'ð', 'ù', 'Â', '×', 'c', 'é', 'Ð', 'Ç', 'g', 'V', 'ñ', '»', 'È', 'M', 'µ', 'm', 'Þ'], ['P', '”', 'K', '`', '¯', '™', '•', 'f', 'n', 'L', 'l', 'd', '¾', 'W', 'a', 'e', 'ÿ', 'Ë', '¼', 'j', '_', 'Ü', '¤', 'k', 'b', 'O', 'T', 'U', 'Z', 'š', 'ù', '®', 'c', 'N', 'Y', 'g', 'm', 'M', 'R', '›'], ['”', 'š', '¯', 'n', '(', '¤', '®', '›', '˜']]
        
    def get_char(self, input):
      return self.map.get(input, False)
  
    def update_preedit(self, preedit):
        # Update the preedit text in the application
        text = IBus.Text.new_from_string(preedit)
        self.update_preedit_text(text, len(preedit), True)

    def send_backspace(self, count):
        # Simulate backspace presses (limited to IBus's capabilities)
        self.pressback.exec(count)
    def clean_context(self):
        self.context = ""
    
    def process_key_event(self, obj, keyval, keycode, state):
                      
        if state not in [16, 17, 0, 1]: #Blocking keyup events and enabling Gnome search writing 
            return False
            
        if keycode in [103, 105, 106, 108, 102, 107, 104, 109]: #Pressing Arrows
            self.clean_context()
            return False
        char = self.get_char(keyval) #Lookup Table
        
        if not char and keycode == 14: #If not a return from char then..
            if self.context: self.context = self.context[:-1]
            return False
        elif not char and keyval ==32:
          self.context = " "
          return False
        elif not char:
            return False  # Let IBus handle the key normally KKKKK 
        if not self.context:
            self.context = char
        if self.context[-1]+char in self.rep[0]:
            char = self.rep[0][self.context[-1]+char]
            #if not self.context == " ": 
            self.send_backspace(1)                
            #else: char = char[-1]
            self.context = char
        
        elif len(self.context)>1 and self.context[-2:]+char in self.rep[1]:
            char = self.rep[1][self.context[-2:]+char]
            self.send_backspace(2)
            self.context = char
        elif len(self.context)>2 and self.context+char in self.rep[2]:
            char = self.rep[2][self.context+char]
            self.send_backspace(3)
            self.context = char
        elif len(self.context)>2: self.context = self.context[1:]+char
        elif self.context[0] in self.rep_ki[1]+self.rep_ki[2]: # Storing context for 3 and 4 char pattern rep.
            self.context += char
        else: self.context = char
        self.commit_text(IBus.Text.new_from_string(char))
        return True  # Key event handled


class EngineFactory(IBus.Factory):
    def __init__(self, bus):
        self.bus = bus
        self.id = 0
        super(EngineFactory, self).__init__(object_path=IBus.PATH_FACTORY,
                                            connection=bus.get_connection())


        bus.get_connection().signal_subscribe('org.freedesktop.DBus',
                                              'org.freedesktop.DBus',
                                              'NameOwnerChanged',
                                              '/org/freedesktop/DBus',
                                              None,
                                              0,
                                              self.name_owner_changed,
                                              bus)

    def do_create_engine(self, engine_name):
        print(engine_name)
        if engine_name == 'bijoy:unicode':
            self.id += 1
            return UnicodeEngine(self.bus, '/com/redhat/IBus/engines/Bijoy/UnicodeEngine'+str(self.id))
        if engine_name == 'bijoy:classic':
            self.id += 1
            return ClassicEngine(self.bus, '/com/redhat/IBus/engines/Bijoy/ClassicEngine'+str(self.id))

        return super(EngineFactory, self).do_create_engine(engine_name)

    def name_owner_changed(self, connection, sender_name, object_path,
                                interface_name, signal_name, parameters,
                                user_data):
        pass


def disconnected(bus):
    IBus.quit()
# Register the engine
def main():
    IBus.init()
    IBus.set_log_handler(True)
    bus = IBus.Bus()
    bus.connect('disconnected', disconnected)
    if not bus.is_connected():
        print("Failed to connect to IBus daemmon.")
        import sys
        sys.exit(1)
    print('started')
    #bus.connect('disconnected', self.__bus_disconnected_cb)
    #factory = IBus.Factory.new(bus.get_connection())
    #factory.add_engine("bijoy:unicode", UnicodeEngine)
    factory = EngineFactory(bus)
    bus.request_name('org.freedesktop.IBus.bijoy_JB', 0)
    #factory.create_engine('bijoy')
    #engine = factory.create_engine('bijoy')
    #if engine:
    #    print('engine created')
    #engine.process_key_event(IBus.KEY_j, 0, 0)
    #else:
    #    print('failed to create')
    IBus.main()

mainloop = GLib.MainLoop()

if __name__ == "__main__":
    main()
