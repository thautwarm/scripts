
from Ruikowa.ObjectRegex.Node import Ref, AstParser, SeqParser, LiteralParser, CharParser, MetaInfo, DependentAstParser
from etoken import token 
import re
namespace     = globals()
recurSearcher = set()
Number = AstParser([SeqParser([LiteralParser('-', name='\'-\'')], atmost = 1),LiteralParser('\d+', name='\'\d+\'', isRegex = True),SeqParser([CharParser('.', name='\'.\''),LiteralParser('\d+', name='\'\d+\'', isRegex = True)], atmost = 1),SeqParser([CharParser('E', name='\'E\''),SeqParser([LiteralParser('-', name='\'-\'')], atmost = 1),LiteralParser('\d+', name='\'\d+\'', isRegex = True)], atmost = 1)], name = 'Number')
Data = AstParser([Ref('Number'),SeqParser([CharParser(',', name='\',\''),Ref('Number')]),SeqParser([LiteralParser('\n', name='\'\n\'')])], name = 'Data', toIgnore = [{},{'\n',','}])
DataSets = AstParser([SeqParser([Ref('Data')])], name = 'DataSets')
Number.compile(namespace, recurSearcher)
Data.compile(namespace, recurSearcher)
DataSets.compile(namespace, recurSearcher)
