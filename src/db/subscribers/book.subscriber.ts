import { EntitySubscriberInterface, EventSubscriber } from "typeorm";
import { TransactionCommitEvent } from "typeorm/subscriber/event/TransactionCommitEvent";

@EventSubscriber()
export class PostSubscriber implements EntitySubscriberInterface<any> {
    // afterLoad(entity: any) {
    //     console.log(entity);
    //     console.log(`${entity.constructor.name}: ${entity.id} `);
    // }

    afterTransactionCommit(event: TransactionCommitEvent) {
        console.log(`AFTER TRANSACTION COMMITTED: `, event);
    }
}