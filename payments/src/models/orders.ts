import mongoose from 'mongoose';
import { OrderStatus } from '@ddticketing/common';




 interface OrderAttrs {
    id: string;
    status: OrderStatus;
    version: number;
    userId: string;
    price: number;
}

interface OrderDoc extends mongoose.Document {
    id: string;
    status: OrderStatus;
    version: number;
    userId: string;
    price: number;
}


interface OrderModel extends mongoose.Model<OrderDoc> {
    build(attrs: OrderAttrs): OrderDoc;
}



const orderSchema = new mongoose.Schema({
    userId: {
        type: String,
        required: true
    },
    status: {   
        type: String,
        required: true
    },
    version: {
        type: Number,
        required: true
    },
    price: {
        type: Number,
        required: true
    }
},{
    optimisticConcurrency: true,
    toJSON: {
        transform(doc, ret: any) {
            ret.id = ret._id;
            delete ret._id;
        }
    }
});
orderSchema.set('versionKey', 'version');

orderSchema.statics.build = (attrs: OrderAttrs) => {
    return new Order({
        _id: attrs.id,
        userId: attrs.userId,
        status: attrs.status,
        version: attrs.version,
        price: attrs.price
    });
};

const Order = mongoose.model<OrderDoc, OrderModel>('Order', orderSchema);

export { Order };

