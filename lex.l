%{
#include <string.h>

/*Definitions of manifest constants*/
enum TAG {
KEYWORD=1,ARITHMETIC_OPERATOR=2,STRING=3,NUMBER = 4,ID=5,UNREC = 999,LOGICAL_OPERATOR=6,CONDITIONAL_OPERATOR=7,OTHER_OPERATOR=8,ASSIGNMENT_OPERATOR=9,DATATYPE=10,INPUT_OUTPUT=11,MACRO=12};

int yyval = -1;

/*Symbol Table*/
struct token{
 char* value;
} entity[1000];

int count = 0;     //number of tokens
//  [ \t\n]+          {printf( "<WHITESPACES   %s>\n", yytext );/* eat up whitespace */}
%}

DIGIT    	[0-9]
ID       	([a-z]|[A-Z]|_)([a-z]|[A-Z]|[0-9]|_)*

%%
main	{printf("Token: <MAIN_FUNCTION , %s >\n",yytext);}
"{"	{printf("Token: <OPEN_PARENTHESIS , %s >\n",yytext);}
"}"	{printf("Token: <CLOSE_PARENTHESIS , %s >\n",yytext);}
"("|")"	{printf("Token: <BRACKET , %s >\n",yytext);}
";"	{printf("Token: <SEMI , %s >\n",yytext);}
"/*"(.|[\r\n])*"*/"|"//".*	{printf("Token: <COMMENT , %s >\n",yytext);}
for|if|"else if"|else|do|while|struct|return|switch|typedef|goto	{return(KEYWORD);}
("int"|"char"|"unsigned"|"void"|"float"|"double")[ \t]"*"?		{return(DATATYPE);}
"bool"|"true"|"false"		{return(MACRO);}
{DIGIT}+    	{ return(NUMBER);}
{ID}        {yyval = (int)installID(); return(ID);}
"+"|"-"|"/"|"%"|"*"	 { return(ARITHMETIC_OPERATOR);}
"|"|"&&"	 { return(LOGICAL_OPERATOR);}
"=="|"<"|">"|"<="|">="	 { return(CONDITIONAL_OPERATOR);}
"+="|"-="|"*="|"/="|"++"|"--"	 { return(OTHER_OPERATOR);}	 
"="	 { return(ASSIGNMENT_OPERATOR);}
#define|#include<[a-z]+.h> {printf("Token: <PREPROCESSOR , %s >\n",yytext);}
","|"\."			{printf("Token: <SPECIAL_SYMBOL , %s >\n",yytext);}
[ \t\n]+          {/* eat up whitespace */}
.           {return(UNREC);}
"printf\(".*"\)"|"scanf\(".*"\)"	{return(INPUT_OUTPUT);}
"\""[^\"]*"\""	{return(STRING);}


%% 
int yywrap(void){return 1;}

int installID(){
char* str = strdup(yytext);
int i;
 for(i=0;i<count;i++){
  if(!strcmp(entity[i].value,str)){
   //already exists in symbol table
   return i;
  }
 }
 int index = count;
 entity[index].value = str;
 count++;
 return index;
}



int main(int argc, char *argv[])
{
    ++argv, --argc;    /* skip argv[0] */    
    yyin = fopen(argv[0], "r");    
    printf("\n\nStart scanning...:\n\n");
    int tok;
    while(tok = yylex()){
      if (tok == NUMBER) {
	/*Integer*/
	printf("Token: <NUMBER , %s >\n",yytext);
      } else if (tok==KEYWORD){
	/*Keywords*/
	printf("Token: <KEYWORD , %s >\n",yytext);
      }else if (tok==ARITHMETIC_OPERATOR){
	/*Keywords*/
	printf("Token: <ARITHMETIC_OPERATOR , %s >\n",yytext);
      } else if (tok==ASSIGNMENT_OPERATOR){
	/*Keywords*/
	printf("Token: <ASSIGNMENT_OPERATOR , %s >\n",yytext);
      } else if (tok==LOGICAL_OPERATOR){
	/*Keywords*/
	printf("Token: <LOGICAL_OPERATOR , %s >\n",yytext);
      } else if (tok==CONDITIONAL_OPERATOR){
	/*Keywords*/
	printf("Token: <CONDITIONAL_OPERATOR , %s >\n",yytext);
      } else if (tok==OTHER_OPERATOR){
	/*Keywords*/
	printf("Token: <OTHER_OPERATOR , %s >\n",yytext);
      } else if(tok == ID){
	/*Identifier*/
	printf("Token: <ID , %d >\n",yyval);
      } else if(tok == STRING){ 
	/*String*/	
	printf("Token: <STRING , %s >\n", yytext);
      }  else if(tok == UNREC){
	printf("Token: <UNKNOWN , %s >\n", yytext); 
      } else if(tok == DATATYPE){
	printf("Token: <DATATYPE , %s >\n", yytext); 
      }else if(tok == INPUT_OUTPUT){
	printf("Token: <INPUT_OUTPUT , %s >\n", yytext); 
      }else if(tok == MACRO){
	printf("Token: <MACRO , %s >\n", yytext); 
      }    else {
	printf("\n");
      }
    }

    printf("\n\nSymbol Table:\n");
    int i;
    for(i=0;i<count;i++){
      printf("entry: %3d, symbol: %12s\n",i,entity[i].value);
    }

    return 0;
}
