import { OrderStatus } from "@ddticketing/common/dist/events/types/order-status";
import mongoose from "mongoose";

interface ticketAttrs{
    title:string;
    price:number;
    id:string;
}

export interface ticketDoc extends mongoose.Document{
    id:string;
    title:string;
    price:number;
    version?:number;
    isReserved():Promise<boolean>
}

interface ticketModel extends mongoose.Model<ticketDoc>{
    build(attrs:ticketAttrs):ticketDoc;
}

const ticketSchema=new mongoose.Schema({
    title:{
        type:String,    
    required:true
    },
    price:{
        type:Number,
        required:true
    },
    version:{
        type:Number,
        
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

ticketSchema.statics.build=(attrs:ticketAttrs)=>{
    return new Ticket({
        _id:attrs.id,
        title:attrs.title,
        price:attrs.price
    });
}

ticketSchema.set('versionKey','version');

ticketSchema.methods.isReserved=async function(){
    const existingOrder=await mongoose.model('Order').findOne({
        ticket:this,
        status:{
            $in:[
                OrderStatus.Created,
                OrderStatus.AwaitingPayment,
                OrderStatus.Complete
            ]
        }
    })
    return !!existingOrder;
}

const Ticket=mongoose.model<ticketDoc,ticketModel>('Ticket',ticketSchema);

export {Ticket}