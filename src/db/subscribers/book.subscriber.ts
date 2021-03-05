import { EntitySubscriberInterface, EventSubscriber, UpdateEvent } from "typeorm";
import { BookController } from "../controllers/book.controller";
@EventSubscriber()
export class BookSubscriber implements EntitySubscriberInterface<any> {
	// constructor(private bookController: BookController) {}
	// afterUpdate(event: UpdateEvent<any>) {

	// 	console.log(event);
	// }
    // afterTransactionCommit(event: TransactionCommitEvent) {
    //     console.log(`AFTER TRANSACTION COMMITTED: `, event);
    // }
}