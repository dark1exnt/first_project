CREATE TABLE rooms (
    id BIGSERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    price_per_night INTEGER NOT NULL CHECK (price_per_night > 0),
    created_at TIMESTAMPZ NOT NULL DEFAULT NOW()
);

CREATE TABLE bookings (
    id BIGSERIAL PRIMARY KEY,
    room_id BIGINT NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
    date_start DATE NOT NULL,
    date_end DATE NOT NULL,
    created_at TIMESTAMPZ NOT NULL DEFAULT NOW(),
    CHECK (date_end > date_start)
);

CREATE INDEX idx_bookings_room_date_start
    ON bookings (room_id, date_start);
