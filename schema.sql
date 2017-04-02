USE stockworks;
CREATE TABLE tone (
   ticker varchar(10),
   recordtime datetime,
   price decimal,
   conscientiousness float,
   confidence float,
   anger float,
   joy float,
   sadness float,
   disgust float,
   emotionalrange float,
   extraversion float,
   tentative float,
   analytical float,
   agreeable float,
   openness float,
   fear float,
   conscientiousness_std float,
   confidence_std float,tone
   anger_std float,
   joy_std float,
   sadness_std float,
   disgust_std float,
   emotionalrange_std float,
   extraversion_std float,
   tentative_std float,
   analytical_std float,
   agreeable_std float,
   openness_std float,
   fear_std float,
   CONSTRAINT pk_tone PRIMARY KEY(ticker, recordtime)
);
CREATE INDEX idx_ticker ON tone (ticker)

