import { Injectable } from '@angular/core';
import * as Bolt from '../bolt/bolt.interface';
@Injectable({
  providedIn: 'root'
})
export class MemberService implements Bolt.ClientService {
	public members: any[] = null;
	public collectionNames: Bolt.CollectionNames = {
		request:	"users",
		response:	"members",
		local:		"members"
	};
}
