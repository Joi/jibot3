export interface BoltCollectionNames {
	request:	string;
	response:	string;
	collection:	string;
}
export interface BoltClientService {
	collectionNames: BoltCollectionNames;
}