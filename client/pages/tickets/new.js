import { useState } from "react";
import useRequest from "../../hooks/use-request";

const NewTicket = () => {

    const [title, setTitle] = useState('');
    const [price, setPrice] = useState('');
    const pageStyle = {
        maxWidth: '500px',
        margin: '40px auto',
        padding: '24px',
        borderRadius: '12px',
        backgroundColor: '#f8f9fa',
        boxShadow: '0 8px 24px rgba(0, 0, 0, 0.08)'
    };

    const titleStyle = {
        textAlign: 'center',
        marginBottom: '24px',
        fontWeight: 600
    };

    const formGroupStyle = {
        marginBottom: '16px'
    };

    const buttonStyle = {
        width: '100%',
        marginTop: '8px'
    };

    const { request, errors } = useRequest({
        url: '/api/tickets/create',
        method: 'post',
        body:{
            title,price
        },
        onSuccess: (ticket) => {
            setTitle('');
            setPrice('');
            alert(`Ticket created successfully with ID: ${ticket.id}`);
        }
    })
    console.log("errors==>",errors)
    const onSubmit = (e) => {
        e.preventDefault();
        request({ title, price });
    }
    const _onBlur = () => {
        const value = parseFloat(price);
        if (isNaN(value)) {
            return;
        }
        setPrice(value.toFixed(2));
    }

    return (
        <div style={pageStyle}>
            <h1 style={titleStyle}>New Ticket</h1>

            <form onSubmit={onSubmit}>
                <div className="form-group" style={formGroupStyle}>
                    <label htmlFor="ticketTitle">Ticket Title</label>
                    <input type="text" className="form-control" onChange={(e) => setTitle(e.target.value)} value={title} id="ticketTitle" placeholder="Enter ticket title" />
                </div>
                <div className="form-group" style={formGroupStyle}>
                    <label htmlFor="ticketPrice">Ticket Price</label>
                    <input type="number" onBlur={_onBlur} className="form-control" onChange={(e) => setPrice(e.target.value)} value={price} id="ticketPrice" placeholder="Enter ticket price" />
                </div>
                <button type="submit" className="btn btn-primary" style={buttonStyle}>Submit</button>
            </form>
           {errors && errors.length > 0 && (
                <div className="alert alert-danger mt-3">
                    <ul>
                        {errors.map((error) => (
                            <li key={error}>{error.message|| error.msg}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default NewTicket