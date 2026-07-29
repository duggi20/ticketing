import  Queue  from "bull";
import {ExpirationCompletedPublisher} from '../events/publisher/Expiration-completed-publisher'
import { natsWrapper } from "../nats-wrapper";

const ExpirationQueue=new Queue('expiration', {
    redis:{
        host:'expiration-redis-svc',
    }
})

ExpirationQueue.process(async(job)=>{
    console.log('I want to publish an expiration event for orderId',job.data.orderId)
    const publisher= new ExpirationCompletedPublisher(natsWrapper.client)
    await publisher.publish({
        orderId: job.data.orderId
    })
})

export {ExpirationQueue}


