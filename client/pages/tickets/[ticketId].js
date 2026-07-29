import React from 'react'
import Link from 'next/link'
import { useRouter } from 'next/router'
import useRequest from '../../hooks/use-request';

const TicketDetail = (props) => {
    const { ticketDetail } = props;
    const router = useRouter();

    const { request, errors } = useRequest({
        url: '/api/orders',
        method: 'post',
        body: { ticketId: ticketDetail.id },
        onSuccess: (order) => {
            console.log("order created==>",order)
            router.push(`/orders/[orderId]`, `/orders/${order.id}`);
        }
    })

    const openOrderDetail = () => {
        request()
    }
    
    return (
        <div>
            <h1>Ticket Detail Page</h1>
            <p><strong>Title:</strong> {ticketDetail.title}</p>
            <p><strong>Price:</strong> ${ticketDetail.price.toFixed(2)}</p>
            <button className="btn btn-primary" onClick={openOrderDetail}>
                Purchase
            </button>
            {errors && (
                <div className="alert alert-danger mt-3" role="alert">
                    {Array.isArray(errors)
                        ? errors.map((error, index) => (
                            <div key={`${error.message || error.msg || 'error'}-${index}`}>
                                {error.message || error.msg || 'Unable to reserve this ticket.'}
                            </div>
                        ))
                        : errors.message || errors.msg || errors}
                </div>
            )}
        </div>
    )
}

TicketDetail.getInitialProps = async (context, client, currentUser) => {
    const { ticketId } = context.query;
    const ticketDetail = await client.get(`/api/tickets/${ticketId}`);
    return { ticketDetail: ticketDetail.data };
}

export default TicketDetail
