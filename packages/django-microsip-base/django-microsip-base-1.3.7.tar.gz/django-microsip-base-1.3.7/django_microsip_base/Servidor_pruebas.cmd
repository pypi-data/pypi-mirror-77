echo off
color 0B
cls
echo 			==================================
echo 			=                                =
echo 			=     SERVIDOR DE PAGINA WEB     =
echo 			=                                =
echo 			=     MODO: PRUEBAS    	         =
echo 			=     POR FAVOR NO CERRAR!!!!    =
echo 			=                                =
echo 			==================================
echo.
echo.
start /B redis/redis-server.exe
python manage_dev.py runserver_plus 0.0.0.0:8001


