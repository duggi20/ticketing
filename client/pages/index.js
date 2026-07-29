 import Link from 'next/link';
import React from 'react'

 
 const Index = (props) => {
  const { currentUser, ticketsList } = props;

  return (
    <div>
        <h1>Welcome to the Home Page</h1>
        {currentUser && <p>Hello, {currentUser.email}!</p>}
        <h2>Tickets</h2>
        <table style={{width: '100%', borderCollapse: 'collapse'}}>
          <thead>
            <tr>
              <th style={{textAlign: 'left', borderBottom: '1px solid #ddd', padding: '8px'}}>Title</th>
              <th style={{textAlign: 'left', borderBottom: '1px solid #ddd', padding: '8px'}}>Price</th>
              <th style={{textAlign: 'left', borderBottom: '1px solid #ddd', padding: '8px'}}>Action</th>
            </tr>
          </thead>
          <tbody>
            {ticketsList && ticketsList.map((ticket) => (
              <tr key={ticket.id}>
                <td style={{padding: '8px', borderBottom: '1px solid #f1f1f1'}}>{ticket.title}</td>
                <td style={{padding: '8px', borderBottom: '1px solid #f1f1f1'}}>${ticket.price.toFixed(2)}</td>
                <td style={{padding: '8px', borderBottom: '1px solid #f1f1f1'}}>
                  <Link href={`/tickets/[ticketId]`} as={`/tickets/${ticket.id}`}>
                    View
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
    </div>
  )
}

Index.getInitialProps = async (context, client, currentUser) => {
  const ticketsList=  await client.get('/api/tickets');
  console.log('ticketsList', ticketsList.data);
  
  return { currentUser, ticketsList: ticketsList.data };
}

export default Index
