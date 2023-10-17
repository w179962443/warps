
from pathlib import Path

from pyhocon import ConfigFactory

conf = ConfigFactory.parse_file('configs/base_config.conf')

print()


WANLISH_DIR = Path(__file__).resolve().parent
conf.root_dir=WANLISH_DIR

str(conf.root_dir)


print()

# pip install -q transformers accelerate bitsandbytes
from transformers import AutoModelForCausalLM, AutoTokenizer

# checkpoint = "D:\\model\\bloomz-560m"

# tokenizer = AutoTokenizer.from_pretrained(checkpoint)
# model = AutoModelForCausalLM.from_pretrained(checkpoint, device_map="auto")

# inputs = tokenizer.encode("你好啊", return_tensors="pt").to("cuda")
# outputs = model.generate(inputs)
# print(tokenizer.decode(outputs[0]))

checkpoint = "D:\\model\\bloom-560m"

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint, device_map="auto")

inputs = tokenizer.encode("你好啊", return_tensors="pt").to("cuda")
outputs = model.generate(inputs)
print(tokenizer.decode(outputs[0]))


print()




