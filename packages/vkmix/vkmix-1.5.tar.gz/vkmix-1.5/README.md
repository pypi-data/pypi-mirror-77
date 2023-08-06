Python wrapper for [vkmix.com API](https://vkmix.com/settings/api). 

[Документация](https://vkmix.readthedocs.io/)
## Installing
`python3 -m pip install git+https://github.com/alekssamos/vkmix.git`

or

`python3 -m pip install vkmix`
### Using
```python3
from vkmix import VkMix

vkm = VkMix("YOURKEY")

print("Баланс: ", vkm.getBalance())

task = vkm.createTask(
	network = "vk",
	section = "likes",
	link = "https://vk.com/wall-139740824_2687166",
	count = 10,
	hourly_limit = 5,
	amount = 5
)
print("Создано задание: ID ", task["id"])

print("Получить все задания на аккаунте: ", vkm.getTasks())
```
## Runing tests
```bash
git clone https://github.com/alekssamos/vkmix.git
cd vkmix
python3 -m pip install -r requirements-dev.txt

python3 -m unittest
# or
python3 -m tox
```
