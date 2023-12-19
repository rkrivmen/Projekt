f=open("tegevus.txt","r",encoding="UTF-8")
ajad={}
highlighted_days={}
for i in f:
    i=i.strip("\n").split(":")
    if i[0] in ajad:
        osa=ajad[i[0]]
        osa.append(i[1::])
        ajad[i[0]]=osa
    else:
        ajad[i[0]]=[i[1::]]
print(ajad)
aeg=ajad["artur"]
print(aeg)
for i in aeg:
    if i[0] in highlighted_days:
        osa=highlighted_days[str(i[0])]
        osa.append([str(i[1]),int(i[2])])
        highlighted_days[str(i[0])]=osa
    else:
        highlighted_days[str(i[0])]=[[str(i[1]),int(i[2])]]
print(highlighted_days)