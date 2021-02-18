export interface BoltCollectionNames {
	request:	string;
	response:	string;
	local:		string;
}
export interface BoltClientService {
	collectionNames: BoltCollectionNames;
}