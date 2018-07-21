import re, traceback, keyword

def pnamedtuple(type_name, field_names, mutable=False):
    def show_listing(s):
        for aline,its_text in enumerate(s.split('\n'), 1):
            print(f' {aline: >3} {its_text.rstrip()}')
            
    # put your code here
    # bind class_definition (used below) to the string constructed for the class 
    def it(iterable):
        used = set()
        for each in iterable:
            if each not in used:
                used.add(each)
                yield each
            else:
                pass

    if type(type_name) != str:
        raise SyntaxError('Type_name must be str')
    else:
        search_pattern = re.compile('^[(A-Z)|(a-z)][\d|\w]*$')
        if search_pattern.match(type_name) == None or type_name in keyword.kwlist:
            raise SyntaxError("Type name must begin with letter")
    
    if type(field_names) not in (str, list):
        raise SyntaxError("Type of fields must be list or str")
    else:
        if type(field_names) == str:
            field_names = field_names.replace(',','').split()
            field_names = list(it(field_names))
        search_pattern = re.compile('^[(A-Z)|(a-z)][\d|\w]*$')
        for each in field_names:
            if each in keyword.kwlist or search_pattern.match(each) == None:
                raise SyntaxError("Fields have to begin with a letter")
    
    def gen_class():
        return 'class {}:\n'.format(type_name)
    
    def gen_init():
        self_vars = ''
        args = ''
        for each in field_names:
            args += '{},'.format(each)
        
        for each in field_names:
            if each == field_names[0]:
                self_vars += 'self.{} = {}'.format(each,each)
            else:
                self_vars += '\n        self.{} = {}'.format(each,each)
        
        final = '''\
    def __init__(self, {}):
        {}
        self._fields = {}
        self._mutable = {}\n'''.format(args,self_vars,str(field_names),str(mutable))

        return final
    def gen_repr():
        header = '''\
    def __repr__(self):
        return '{}('''.format(type_name)
        inside = ''
        outside = ''
        
        for each in field_names:
            inside += ('{}={{{}}},').format(each,each)
        inside = inside[:-1]
        header += (inside + ')\'')
        
        for each in field_names:
            outside += ('{}=self.{},').format(each,each)
        outside = '.format(' + outside[:-1]+')'
        header += (outside+'\n')
        
        return header
        
        #old code
        '''
        inside = ''
        outside = ''
        
        for each in field_names:
            inside += ('{}={{{}}},').format(each,each)
            outside += ('{}=self.{},').format(each,each)
        inside = inside[:-1] + ')\'.format('
        outside = outside[:-1] + ")'"
        header = \
    def __repr__(self):
        return '{}({}{}.format(type_name,inside,outside)
        return header

        header = \
    def __repr__(self):
        return '{}(.format(type_name)
        
        inside = ''
        outside = ''
        
        for each in field_names:
            inside += (each + '={' + each + '},')
        header += (inside[:-1] + ')\'.format(')
        
        for each in field_names:
            outside += '{} = self.{},'.format(each,each)
        header += (outside[:-1] + ")'")
        
        return header'''

    def gen_accessors():
        final = ''
        for each in field_names:
            final += '''\
    def get_{}(self):
        return self.{}\n\n'''.format(each, each)
        
        return final
    
    def gen_getitem():
        header = '''\
    def __getitem__(self,val):
        if type(val) in (int,str):
            if type(val) == int:
                if val in range(len(self._fields)):
                    new = self._fields[val]
                    final = 'self.get_{}()'.format(new)
                    final = eval(final)
                    return final
                else:
                    raise IndexError('Index is out of range')
            elif type(val) == str:
                if val not in self.__dict__.keys():
                    raise IndexError('Index is not valid')
                else:
                    return self.__dict__[val]
        else:
            raise IndexError('Index type must be str or int')\n\n'''
        return header
    
    def gen_equals():
        header = '''\
    def __eq__(self,right):
        counter = 0
        if type(self) == type(right):
            for each in range(len(self._fields)):
                if self._fields[each] == right._fields[each]:
                    counter += 1
        if counter == len(self._fields):
            return True
        else:
            return False\n'''
        return header
    
    def gen_replace():
        header = '''\
    def _replace(self, **kargs):
        for each in kargs.keys():
            if each not in self._fields:
                raise TypeError('Not a valid field name: {{}}'.format(each))
        if self._mutable:
            for each in kargs.keys():
                self.__dict__[each] = kargs[each]
        else:
            header = '{type}('        
            for each in kargs.items():
                header += str(each) + ','
            return eval(header[:-1] + ')')'''.format(type = type_name)
       
        return header


    class_definition = '''\
class {}:\n{}\n{}\n{}\n{}\n{}\n{}
'''.format(type_name,gen_init(),gen_repr(),gen_accessors(),gen_getitem(),gen_equals(),gen_replace())

    # For initial debugging, remove comment to show the source code for the clas
    #show_listing(class_definition)
    
    # Execute the class_definition string in a local name space; later, bind the
    #   source_code name in its dictionary to the class_defintion; return the
    #   class object created; if there is a syntax error, list the class and
    #   also show the error
    name_space = dict(__name__ =  f'pnamedtuple_{type_name}')
    try:
        exec(class_definition,name_space)
        name_space[type_name].source_code = class_definition
    except [TypeError, SyntaxError]:
        show_listing(class_definition)
        traceback.print_exc()
    return name_space[type_name]


    
if __name__ == '__main__':
    # Test pnamedtuple in script below using Point = pnamedtuple('Point', 'x y')
    
    #driver tests
    import driver
    driver.default_file_name = 'bscp3W18.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
