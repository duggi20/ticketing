import { useEffect, useRef, useState } from "react";
import { loadStripe } from '@stripe/stripe-js';
import useRequest from '../../hooks/use-request';

const stripePromise = loadStripe('pk_test_51Tu5tkKARYWrfFMsey2kmSb39gxXgmkBAHCz0gslAqaWOLW3zzFJPYwRSO1WubCdPSMFJ2AVmBBJKV5gWeMOZlHS00bxLIyHkA');

const OrderDetail=({orderDetail,currentUser})=>{
  const [timeLeft,setTimeLeft]=useState(0);
  const [card, setCard] = useState(null);
  const [stripeError, setStripeError] = useState(null);
  const cardElementRef = useRef(null);

  const { request, errors } = useRequest({
    url: '/api/payments',
    method: 'post',
    onSuccess: (data) => {
     console.log("data==>",data)
    },
  });

  useEffect(()=>{
   const calculateTimeLeft=()=>{
    let millisecLeft=new Date(orderDetail.expiresAt)-new Date();
    setTimeLeft(Math.round(millisecLeft/1000));
   }

   calculateTimeLeft()
   setInterval(calculateTimeLeft,1000)

},[])

  useEffect(() => {
    let mounted = true;
    let cardElement;

    stripePromise.then((stripe) => {
      if (!stripe || !mounted || !cardElementRef.current) return;

      const elements = stripe.elements();
      cardElement = elements.create('card');
      cardElement.mount(cardElementRef.current);
      setCard(cardElement);
    });

    return () => {
      mounted = false;
      cardElement?.unmount();
    };
  }, []);

  const checkoutStripe = async () => {
    if (!card) return;

    setStripeError(null);
    const stripe = await stripePromise;
    if (!stripe) {
      setStripeError('Stripe could not be loaded. Please try again.');
      return;
    }

    const { token, error } = await stripe.createToken(card);
    if (error) {
      setStripeError(error.message);
      return;
    }
    console.log("token==>",token)

    await request({ token: token.id, orderId: orderDetail.id });
  };

if(timeLeft<0){
    return(
        <div className="alert alert-danger mt-3" role="alert">
            order Expired!
        </div>
    )
}

    return(
        <div>
            <h1>Order Detail Page</h1>
            <p>Time Left: {timeLeft} seconds</p>
            <p>{orderDetail.ticket.title}</p>
            <p>{orderDetail.ticket.price}</p>
            <div className="mb-3" ref={cardElementRef} />
            <button onClick={checkoutStripe}  className='btn btn-primary'>
              Pay Now
            </button>
            {(stripeError || errors) && (
              <div className="alert alert-danger mt-3" role="alert">
                {stripeError || (Array.isArray(errors) ? errors.map((error) => error.message || error.msg).join(', ') : errors)}
              </div>
            )}
        </div>
    )
}


OrderDetail.getInitialProps=async(context,client,currentUser)=>{
    const {orderId}=context.query;
    const orderDetail=await client.get(`/api/orders/${orderId}`);
    return {orderDetail:orderDetail.data,currentUser};
}

export default OrderDetail;
