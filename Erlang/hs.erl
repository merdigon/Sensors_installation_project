-module(hs).
-compile([export_all]).
-include("mochiweb-master/include/internal.hrl").

start()->
	SerwerID=spawn(hs, serv,[]),
	spawn(hs, udpMessServer, [SerwerID]),
	{serwer,start}.

serv() ->
	HTTPID = spawn(hs, httpMessServer, []),
	receiveMess(self(),HTTPID).

receiveMess(ServID, SendServID) ->
	receive			
		{_, {X, SID, registering}} -> SendServID!{self(), {transSensToString(X), SID, registering}};		
		{_, {thermometer, SID, temperature, Temper}} -> SendServID!{self(), {transSensToString(thermometer), SID, temperature, Temper}};
		{_, {X, N, Op, Value}} -> SendServID!{self(), {transSensToString(X), N, Op, Value}}
	end,
	receiveMess(ServID, SendServID).


%sensory
window(ServID, SelfID, Open, Broken) ->
	receive
		{_, {registering}} -> ServID!{self(),{window, SelfID, registering}}, NOpen = Open, NBroken = Broken;
		{_, {open}} when Open == false -> ServID!{self(),{window, SelfID, open, true}}, NOpen = true, NBroken = Broken;
		{_, {open}} when Open == true -> ServID!{self(),{window, SelfID, open, false}}, NOpen = false, NBroken = Broken;
		{_, {broken}} when Broken == false -> ServID!{self(),{window, SelfID, broken, true}}, NOpen = Open, NBroken = true;
		{_, {broken}} when Broken == true -> ServID!{self(),{window, SelfID, broken, false}}, NOpen = Open, NBroken = false;
		{_, {killYourself}} -> io:format("Sensor okno ~p zamordowany!", [SelfID]), exit(window_dead), NOpen = Open, NBroken = Broken
	end,
	window(ServID, SelfID, NOpen, NBroken).

door(ServID, SelfID, Open, Locked) ->
	receive
		{_, {registering}} -> ServID!{self(),{door, SelfID, registering}}, NOpen = Open, NLocked = Locked;
		{_, {open}} when (Open == false) and (Locked == false) -> ServID!{self(),{door, SelfID, open, true}}, NOpen = true, NLocked = Locked;
		{_, {open}} when Open == true -> ServID!{self(),{door, SelfID, open, false}}, NOpen = false, NLocked = Locked;
		{_, {lock}} when (Locked == false) and (Open == false) -> ServID!{self(),{door, SelfID, lock, true}}, NOpen = Open, NLocked = true;
		{_, {lock}} when Locked == true -> ServID!{self(),{door, SelfID, lock, false}}, NOpen = Open, NLocked = false;
		{_, {killYourself}} -> io:format("Sensor drzwi ~p zamordowany!", [SelfID]), exit(door_dead), NOpen = Open, NLocked = Locked
	end,
	door(ServID, SelfID, NOpen, NLocked).

thermometer(ServID, SelfID, Temp) ->
	receive
		{_, {registering}} -> ServID!{self(),{thermometer, SelfID, registering}}, NTemp = Temp;
		{_, {temperature, X}} -> ServID!{self(),{thermometer, SelfID, temperature, X}}, NTemp = X;
		{_, {killYourself}} -> io:format("Sensor termometr ~p zamordowany!", [SelfID]), exit(thermometer_dead), NTemp = Temp
	end,
	thermometer(ServID, SelfID, NTemp).

smoke(ServID, SelfID, Detect) ->
	receive		
		{_, {registering}} -> ServID!{self(),{smoke, SelfID, registering}}, NDetect = Detect;
		{_, {detect}} when Detect == false -> ServID!{self(),{smoke, SelfID, detect, true}}, NDetect = true;
		{_, {detect}} when Detect == true -> ServID!{self(),{smoke, SelfID, detect, false}}, NDetect = false;
		{_, {killYourself}} -> io:format("Sensor czujnik dymu ~p zamordowany!", [SelfID]), exit(smoke_dead), NDetect = Detect
	end,
	smoke(ServID, SelfID, NDetect).


%%%Obsluga odbierania wiadomosci

%postawienie procesu obslugi udp
udpMessServer(ServID) ->
	try
		{ok, Sock} = gen_udp:open(8798, [binary, {active,false}]),
		udpMessReceiving(ServID, Sock, [])
	catch
		Exc:Reas -> {caught, Exc, Reas}
	end.  

%odbieranie wiadomości przez serwer
udpMessReceiving(ServID, Socket, L) ->
	try
		{ok, {_,_,MessBin}} = gen_udp:recv(Socket, 0),
		DecMess = decodeJson(cutSpaces(binary_to_list(MessBin))),
		SensList = udpMessPatternMatcher(DecMess, L, ServID),
		udpMessReceiving(ServID, Socket, SensList)		
	catch
		Exc:Reas -> {caught, Exc, Reas}
	end.  



%%%zamiana wzorca wiadomości udp na standard serwera
 
%rozpoznawanie typu wiadomosci
udpMessPatternMatcher([{"signal","add_sensor"}|T], L, ServID) ->  registerSensor(T, L, ServID);
udpMessPatternMatcher([{"signal","kill_sensor"}|T], L, ServID) ->  killSensor(T, L, ServID);
udpMessPatternMatcher([{"signal","change_status"}|T], L, _) -> changeStatus(T, L), L;
udpMessPatternMatcher(_,L,_) -> io:format("Nie rozpoznano rozkazu udp!"), L.
	
%rejestrowanie sensora
registerSensor([{"sensor_type","Door"}|_], L, ServID) -> registerDoor(L, ServID);
registerSensor([{"sensor_type","Window"}|_], L, ServID) -> registerWindow(L, ServID);
registerSensor([{"sensor_type","Thermometer"}|_], L, ServID) -> registerThermometer(L, ServID);
registerSensor([{"sensor_type","Smoke"}|_], L, ServID) -> registerSmoke(L, ServID);
registerSensor([{"sensor_type",_}|_], L,_) -> io:format("Nierozpoznawalny typ sensora!"), L;
registerSensor(_,_,_) -> io:format("Niepoprawny typ rozkazu rejestracji").

%rejestracja sensorow
registerDoor(L, ServID) ->
	ID = nextSensorId(L),
	DoorID = spawn(hs, door, [ServID, ID, false, false]),
	DoorID!{self(),{registering}},
	io:format("Zarejestrowano ~p", [ID]),
	[{door, DoorID, ID}|L].

registerWindow(L, ServID) ->
	ID = nextSensorId(L),
	WindowID = spawn(hs, window, [ServID, ID, false, false]),
	WindowID!{self(),{registering}},
	io:format("Zarejestrowano ~p", [ID]),
	[{window, WindowID, ID}|L].

registerThermometer(L, ServID) ->
	ID = nextSensorId(L),
	ThermometerID = spawn(hs, thermometer, [ServID, ID, 23]),
	ThermometerID!{self(),{registering}},
	io:format("Zarejestrowano ~p", [ID]),
	[{thermometer, ThermometerID, ID}|L].

registerSmoke(L, ServID) ->
	ID = nextSensorId(L),
	SmokeID = spawn(hs, smoke, [ServID, ID, false]),
	SmokeID!{self(),{registering}},
	io:format("Zarejestrowano ~p", [ID]),
	[{smoke, SmokeID, ID}|L].

%ubijanie sensorow
killSensor([{"sensor_id",X}|_],L,_) -> killSensorWithID(L,stringToInt(X)).

killSensorWithID([],_) -> [];
killSensorWithID([{_,PID,X}|T],ID) when X == ID -> PID!{self(), {killYourself}}, killSensorWithID(T,ID) ;
killSensorWithID([X|T],ID) -> [X] ++ killSensorWithID(T,ID).

%zamiana statusow sensorow
changeStatus([{"sensor_id",X}|T],L) -> changeSensorStatus(findSensor(L, stringToInt(X)), T).

changeSensorStatus(PID, [{"option","Temperature"},X|_]) -> changeTemperature(PID, X);
changeSensorStatus(PID, [{"option",X}|_]) -> PID!{self(), {transStringToOper(X)}};
changeSensorStatus(_, [{X,_}|_]) -> io:format("Niewlasciwy format wiadomosci json: ~p", [X]).

changeTemperature(PID, {"value",X}) -> PID!{self(), {temperature, stringToInt(X)}}.

%%%%wysylanie wiadomosci

httpMessServer() ->
	try
		ssl:start(),
		application:start(inets)
	of
		_ -> httpMessSender()
	catch
		Exc:Reas -> {caught, Exc, Reas}
	end.  

httpMessSender() ->
	receive
		{_, {X, SID, registering}} -> httpc:request(lists:flatten("http://25.104.80.226:8000/api/sensor_register/"++io_lib:format("~p",[SID])++"/"
						++X++"/")), 
						io:format("Http: rejestracja ~p~p~n", [X, SID]);
		{_, {X, SID, temperature, T}} -> httpc:request(lists:flatten("http://25.104.80.226:8000/api/value_change/"++io_lib:format("~p", [SID])++"/"++transOperToString(temperature)++"/"++io_lib:format("~p", [T])++"/")),
						io:format("Http: Operacja temperature ~p ~p~p~n", [T, X, SID]);
		{_, {X, SID, Op, Value}} -> 		httpc:request(
		lists:flatten("http://25.104.80.226:8000/api/status_change/"++io_lib:format("~p", [SID])++"/"++transOperToString(Op)++"/"++io_lib:format("~p", [Value])++"/")),
						io:format("Http: Operacja ~p ~p~p~n", [Op, X, SID])
	end,
	httpMessSender().


%%%funkcje pomocnicze

% dekodowanie jsona
decodeJson(X) -> decodeJsonDeep(string:tokens(X, "{,}")).

decodeJsonDeep([]) -> [];
decodeJsonDeep([X|L]) -> list2ToTrums(string:tokens(X,"\":")) ++ decodeJsonDeep(L).

list2ToTrums([X,Y]) -> [{X, Y}].

%kolejne wolne id sensorów
nextSensorId([]) -> 1;
nextSensorId(L) -> maxSensorId(L) + 1.

% maksymalne zarejestrowane id
maxSensorId(L) -> lists:max(lists:map(fun({_,_,X}) -> X end, L)).

%znajdowanie PID sensora po ID
findSensor([], _) -> io:format("Nie znaleziono sensora o danym ID");
findSensor([{_, PID, ID}|_], ID) -> PID;
findSensor([{_,_,_}|T], FID) -> findSensor(T,FID).

%wydostawanie cześci przed przecinkiem
stringToInt(X) -> getInt(string:to_integer(X)).
getInt({X,_}) -> X.

%tlumaczenie stringa na czynnosc
transStringToOper("Open") -> open;
transStringToOper("Broken") -> broken;
transStringToOper("Lock") -> lock;
transStringToOper("Temperature") -> temperature;
transStringToOper("Detect") -> detect;
transStringToOper(X) -> io:format("Nieobslugiwana operacja: ~p", [X]).

%tlumaczenie czynnosci na stringa
transOperToString(open) -> "Open";
transOperToString(broken) -> "Broken";
transOperToString(lock) -> "Lock";
transOperToString(detect) -> "Detect";
transOperToString(temperature) -> "Temperature".

%tłumaczenie sensora na string
transSensToString(window) -> "Window";
transSensToString(door) -> "Door";
transSensToString(thermometer) -> "Thermometer";
transSensToString(smoke) -> "Smoke";
transSensToString(_) -> io:format("Złe tłumacznie sensora!").	 

%usuwanie spacji
cutSpaces([]) -> [];
cutSpaces([' '|L]) -> cutSpaces(L);
cutSpaces([X|L]) -> [X] ++ cutSpaces(L).  
