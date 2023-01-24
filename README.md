# TelAnalysis
[![asciicast](https://user-images.githubusercontent.com/107117398/213977412-12138f32-e736-434f-9dd4-aed7df895aad.jpg)](https://user-images.githubusercontent.com/107117398/210658121-01c8eac5-ef5b-4b1d-a178-90e31d2b7071.mp4)
# 
![image](https://user-images.githubusercontent.com/107117398/209858730-fe6ff0a3-9fcd-4d13-be6a-3f2a6bdd198b.png)
# TelAnalysis - Telegram Analysis tool
_______
###### Установка / Installing.
```
pip install -r requirements
python main.py
```
_______
###### Menu
```
1 - Make graph and tables for Gephi. Import nodes.csv and edges.csv to Gephi.
2 - Quantitative text analysis [Users & all chat]
3 - Channel Analysis
```
_______
###### Q/A
```
where can I get the file for analysis? Go to the telegram chat and archive it in json, then specify the json file in the tool.
if json weighs more than 200 mb, then you need to change in the sources the call of the explorer automatically selecting the file or entering from the console (will be fixed)
где взять файл для анализа? Зайдите в чат телеграма и архивируйте его в json, далее файл json указывайте в инструменте.
если json  весит более 200 мб, то нужно изменить в исходниках вызов проводника автоматический выбор файла или ввод из консоли(будет исправлено)
```
_______
My Telegram Channel - [@telanalysis](https://t.me/telanalysis).
old channel - [@mav1_notes](https://t.me/mav1_notes).
if you  want help me, sent message in xmpp: lle@disroot.org
_______
###### Version Beta


```
Not all functionality can work perfectly, create an issue, write in the telegram. Channel analysis may not work.
```
_______
```
To do:
Automatic archiving of the chat by link. 
Improved graph generation mechanics.
Add statistics for graphs.
add statistics in Quantitative Analysis.
Fix bugs Improve filtering Definition of Context Sentiment: Total Chat, Per User.
Improved visualization of the interactions of some users with others with interactive selection.
It is possible to connect additional tools and databases for output - comparison of information.
Stylo & Volume analysis-comparison of several chat channels (Suppose there is a main chat and it is compared with another 10 channels, which channel is more similar in various parameters in style - vocabulary with the main one)
```
