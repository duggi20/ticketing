import mongoose from "mongoose";
import {OrderStatus} from '@ddticketing/common'
import { ticketDoc } from "./ticket";



interface OrderAttrs{
    userId:string;
    status:OrderStatus;
    expiresAt:Date;
    ticket:ticketDoc
}


interface OrderDoc extends mongoose.Document{
    id: string;
    userId:string;
    status:OrderStatus;
    expiresAt:Date;
    version:number;
    ticket:ticketDoc
}

interface OrderModel extends mongoose.Model<OrderDoc>{
    build(attrs:OrderAttrs):OrderDoc;
}


const orderSchema=new mongoose.Schema({
    userId:{
        type:String,
        required:true
    },
    status:{
        type:String,
        enum:Object.values(OrderStatus),
        required:true,
        default:OrderStatus.Created
    },
    expiresAt:{
        type:mongoose.Schema.Types.Date,

    },
    ticket:{
        type:mongoose.Schema.Types.ObjectId,
         ref:'Ticket'
    }
},{
    optimisticConcurrency: true,
    toJSON:{
        transform(doc,ret){
            (ret as any).id = ret._id;
            delete (ret as any)._id;
        }
    }
});
orderSchema.set('versionKey','version');
orderSchema.statics.build=(attrs:OrderAttrs)=>{
    return new Order(attrs);
}

const Order=mongoose.model<OrderDoc,OrderModel>('Order',orderSchema);

export {Order}