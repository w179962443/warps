import time 
import datetime 
import tiktoken
import json 
import openai 


class ChatgptConfig:
    model :str 
    temperature:float 
    n:int 
    max_tokens:int 
    api_key:str 

    

token_limit_dict={
    "gpt-3.5-turbo":10000,
    "gpt-4":10000,
    "gpt-3.5-turbo-16k":100000
}
class Tokennizer(object):

    def __init__(self,model_name):
        super().__init__()
        self.encoding = tiktoken.encoding_for_model(model_name)

    def num_tokens_from_string(self,query_string: str) -> int:
        """Returns the number of tokens in a text string."""
        num_tokens = len(self.encoding.encode(query_string))
        return num_tokens

#每一批chatgpt参数对应一个agent。
class ChatgptAgent:

    def __init__(self,logger) -> None:
        self.logger=logger 

    def check_limit(self):
        now=datetime.datetime.now()
        while len(self.chatgpt_hist_list)>0 and (now-self.chatgpt_hist_list[0][0]).seconds>self.second_limit:
            self.chatgpt_hist_list.pop(0)
        total_tokens=0
        for e in self.chatgpt_hist_list:
            total_tokens+=e[1]
        if total_tokens>self.token_limit:
            time.sleep(30)
            print("tokens overloaded.openai sleep 30s") 

    def process_history_to_messages(self,history):
        messages=[
                {"role": "system", "content":self.system},
                {"role": "user", "content": prompt}
        ]
        tokens=self.tokenizer.num_tokens_from_string(self.system)+self.tokenizer.num_tokens_from_string(prompt)
        #assert tokens<4096

        if use_history:
            tl=[]
            for q,a in reversed(new_history):
                new_tokens=self.tokenizer.num_tokens_from_string(q)+self.tokenizer.num_tokens_from_string(a)
                if "16k" in self.openai_model and tokens+new_tokens>16384:
                    break
                elif "16k" not in self.openai_model and tokens+new_tokens>4096:
                    break 
                else:
                    tl=[{"role": "user", "content": q},{"role": "assistant", "content": a}]+tl
                    tokens+=new_tokens
            messages=[messages[0]] + tl +[messages[1]]
        return messages 

    def chatgpt_qa(self,query,history,use_histroy=False,streaming=False):
        self.check_limit()

        messages=self.process_history_to_messages()
        create_dict={}
            
        count=0
        success_flag=False
        while count<3:
            try:
                response =openai.ChatCompletion.create(**create_dict)
                success_flag=True 
                break 
            except Exception as e:
                count+=1
                self.logger.exception(e)
                print("raised exception. retry after 15s")
                time.sleep(15)
        if success_flag:
            if streaming:
                line=""
                for chunk in response:
                    temp=json.loads(str(chunk.choices[0].delta))
                    res=temp["content"] if "content" in temp else ""
                    line+=res
                    yield res,{}
                self.chatgpt_hist_list.append([datetime.datetime.now(),len(line)+len(self.system)+len(prompt)])   
                yield "<finish>",{"answer":,"query":query,"messages":messages,"total_tokens":1}    
            else:
                line= response['choices'][0]['message']['content']
                tokens=response['usage']['total_tokens'] 

                self.chatgpt_hist_list.append([datetime.datetime.now(),tokens])   

                yield line,{"answer":,"query":query,"messages":messages,"total_tokens":1}


    @classmethod
    def create_chatgpt_agent(config:ChatgptConfig):
        
        return ChatgptAgent()
