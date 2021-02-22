import { Injectable } from '@angular/core';
import * as Bolt from '@modules/slack/bolt.interface';
@Injectable({
  	providedIn: 'root'
})
export class ConversationService implements Bolt.ClientService {
	public conversations: any[] = null;
	public collectionNames: Bolt.CollectionNames = {
		request:	"conversations",
		response:	"channels",
		local:		"conversations",
	};
}
