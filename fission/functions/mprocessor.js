module.exports = async function (context) {
  console.log(`Processed an air quality observation`);
  return {
    status: 200,
    body: JSON.stringify (context.request.body.features.map ((feat) => {
        return [{
          id: feat.properties.id,
          created_at: feat.properties.created_at,
          content: feat.properties.content,
          account: feat.properties.account,
        }];
      }
    ))
  };
}
