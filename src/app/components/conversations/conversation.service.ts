import { Injectable } from '@angular/core';
import { BoltClientService, BoltCollectionNames } from '@app/interfaces/bolt-client-service';
@Injectable({
  	providedIn: 'root'
})
export class ConversationService implements BoltClientService {
	public conversations: any[] = null;
	public collectionNames: BoltCollectionNames = {
		request:	"conversations",
		response:	"channels",
		collection:	"conversations",
	};
}
