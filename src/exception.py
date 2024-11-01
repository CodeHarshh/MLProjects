import sys  #it will contain all information about the errors
import logging
from logger import logging

def error_messeage_details(error,error_details:sys):
   _,_,exc_tb= error_details.exc_info() #it will give 3 output , but we need 3rd one it give where exp occure which line
   file_name=exc_tb.tb_frame.f_code.co_filename
   error_message="error ooccur in python script name [{0}] line number [{1}] error message [{2}]".format(
       file_name,exc_tb.tb_lineno,str(error)
   )
  
   return error_message

class CustomException(Exception):
  def __init__(self, error_message,error_detail:sys):
     super().__init__(error_message)
     self.error_message=error_messeage_details(error_message,error_details=error_detail)
      
  def __str__(self):
     return self.error_message 
      


if __name__=="__main__":
    try:
        a=2/0 
    except Exception as e :
        raise CustomException(e,sys)