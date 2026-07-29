import mongoose from "mongoose";
import { PasswordHashing } from "../services/PasswordHashing";


interface UserAttrs {
    email: string;
    password: string;
}  

interface UserModel extends mongoose.Model<UserDoc> {
    build(attrs: UserAttrs): UserDoc;
}

interface UserDoc extends mongoose.Document {
    id: any;
    email: string;
    password: string;
}

const userSchema = new mongoose.Schema({
    email: {
        type: String,   
        required: true,
        unique: true
    },
    password: {
        type: String,
        required: true
    }
}, {
    toJSON: {
        transform(doc: UserDoc, ret: Record<string, any>) {
            ret.id = ret._id;
            delete ret._id;
            delete ret.password;
            delete ret.__v;
        }
    }
});

userSchema.pre('save', async function () {
    if (this.isModified('password')) {
        const hashed = await PasswordHashing.toHash(this.get('password'));
        this.set('password', hashed);
    }
});

userSchema.statics.build = (attrs: UserAttrs) => {
    return new User(attrs);
}


const User = mongoose.model<UserDoc, UserModel>('User', userSchema);

export { User };