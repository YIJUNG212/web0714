import pygal_maps_world.maps

worldMap=pygal_maps_world.maps.World()
#上方標題
worldMap.title='China in the Map '
#左方備註
worldMap.add('China',['cn'])

#可以存檔
#存檔路徑是這個py檔所在資料夾
worldMap.render_to_file('out1_17.svg')