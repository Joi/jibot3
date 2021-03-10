export interface Event {
	name:		string;
	callback:	Function;
}
export interface Message extends Event {
	regex?:	any;
}
export interface CollectionNames {
	request:	string;
	response:	string;
	local:		string;
}
export interface ClientService {
	collectionNames: CollectionNames;
}