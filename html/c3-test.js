var chart = c3.generate({
  bindto: '#chart',
    size: {
        height: 500
    },
data: {
	xFormat: '%Y-%m-%dT%H:%M:%SZ',
        url: '/Log.txt',
        mimeType: 'json',

            keys: {
                x: 'time', // it's possible to specify 'x' when category axis
                value: ['cpu', 'temp', 'humid', 'pressure', 'AmbientLight','red', 'green', 'blue' ],
            },
            axes: {
                cpu: 'y',
                temp: 'y',
                humid: 'y',
                pressure: 'y2',
                AmbientLight: 'y2',
                red: 'y2',
                blue: 'y2',
                green: 'y2'
            },
            type: 'spline'
        },
        point: {
                show:false
        },
        subchart: {
                show:true
        },
    color: {
        pattern: ['#1f77b4', '#0ec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#ff0000', '#00ff00', '#0000ff']
    },
        axis: {
            x: {
                type: 'timeseries',
                label: 'date/time UTC',
                tick: {
                    format: '%Y-%m-%dT%H:%M:%SZ',
                    rotate: 30,
                    count: 8,
                    fit: true

		}
            },
            y: {
                    label: 'cpu,temp,humid'
            },
            y2: {
                    label: 'pressure,Lights',
                    show: true
            }
        }
}
);
