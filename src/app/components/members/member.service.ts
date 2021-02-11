import { Injectable } from '@angular/core';
import { BoltClientService, BoltCollectionNames } from '@app/interfaces/bolt-client-service';
@Injectable({
  providedIn: 'root'
})
export class MemberService implements BoltClientService {
	public members: any[] = null;
	public collectionNames: BoltCollectionNames = {
		request:	"users",
		response:	"members",
		collection:	"members"
	};
}
