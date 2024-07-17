% Function to monitor CSV file for latest values
function monitorCSVFile(csvFilePath, timestampColumn, dataColumn, pauseDuration)
    try
        % Create variables to store latest values
        time = ''; % Initialize empty string for time
        dataValue = int64(NaN); % Initialize with NaN as long type

        while true
            % Read the entire CSV file
            opts = detectImportOptions(csvFilePath);
            opts.VariableNamesLine = 1; % Assumes variable names are in the first row
            data = readtable(csvFilePath, opts);

            % Extract the last row (latest values)
            latestIndex = height(data); % Index of the last row
            latestRow = data(latestIndex, :);

            % Extract specific columns from the latest row
            latestTimestamp = latestRow.(timestampColumn);
            latestDataValue = latestRow.(dataColumn);

            % Format timestamp to hh:mm:ss
            formattedTime = datestr(datetime(latestTimestamp, 'InputFormat', 'dd-MM-yyyy HH:mm:ss'), 'HH:MM:SS');

            % Update variables with latest values
            time = formattedTime; % Formatted time string
            dataValue = int64(latestDataValue); % Convert to long type

            % Display the latest values
            disp(['Latest Timestamp: ', time]);
            disp(['Latest Data Value: ', num2str(dataValue)]);

            % Pause for some time before checking again
            pause(pauseDuration); % Pause for specified duration
        end

    catch ME
        disp(['Error reading CSV file: ', ME.message]);
    end
end

% Example usage:
csvFilePath = 'C:\Users\91857\Desktop\bits\pythonProject2\solar_irradiation_data.csv';
timestampColumn = 'Timestamp'; % Column name for timestamps
dataColumn = 'SolarIrradiation'; % Column name for data values
pauseDuration = 60; % Pause duration in seconds (adjust as needed)

% Call the function
monitorCSVFile(csvFilePath, timestampColumn, dataColumn, pauseDuration);
